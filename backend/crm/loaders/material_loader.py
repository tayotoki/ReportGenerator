from django.db import transaction
from django.shortcuts import get_object_or_404

from crm.loaders import BaseLoader

from materials.models import Material, SimilarMaterialToRequest
from request.models import Request


class MaterialLoader(BaseLoader):
    def load_data_from_crm(self):
        for table in self.client.get_tables(
            names=list(self.converter.FIELDS_MAPPER.values()),
            header=0,
        ):
            raw_data = table.to_dict(orient="records")
            materials_to_create = []
            materials_to_update = {}

            similar_materials = {}

            material_codes = set(self.model.objects.values_list("code", flat=True))

            for data in raw_data:
                converted_data: dict = dict(self.converter(data=data))

                if not self.converter.check_fields(converted_data):
                    continue

                similar_materials_data: list[dict] = converted_data.pop("similar")
                request_number: str = converted_data.pop("number")
                code: int = int(data[self.converter.FIELDS_MAPPER["code"]])

                similar_materials[request_number] = {
                    "code": code,
                    "similar_data": similar_materials_data,
                }

                if code in material_codes:
                    materials_to_update[code] = dict(converted_data)
                else:
                    materials_to_create.append(self.model(**converted_data))
            self.bulk_create(instances=materials_to_create)
            self.bulk_update(instances_data=materials_to_update)
            self.create_or_update_similar(similar_materials)

    def bulk_update(self, instances_data: dict[str, dict]):
        super().bulk_update(instances_data=instances_data)

        if instances_data:
            update_instances = self.model._base_manager.filter(code__in=instances_data)
            for instance in update_instances:
                for field_name, field_value in instances_data[instance.code].items():
                    setattr(instance, field_name, field_value)

            self.model._base_manager.bulk_update(update_instances, fields=self.converter.UPDATE_FIELDS)

            self.count_updated_objects = len(instances_data)

    def create_or_update_similar(self, similar_materials: dict[str, dict]):
        """Добавление похожих материалов к заявке"""

        materials = []
        similar = []

        codes = set(self.model.objects.values_list("code", flat=True))

        for request_number in similar_materials:
            request = get_object_or_404(Request, number=request_number)

            for material in similar_materials[request_number]["similar_data"]:
                if int(material["code"]) not in codes:
                    obj = Material(
                        code=material["code"],
                        full_name=material["full_name"],
                        unit=material["unit"]
                    )
                    materials.append(obj)

                    similar_obj = SimilarMaterialToRequest(
                        request=request,
                        similar=obj,
                        accuracy=material["accuracy"],
                    )

                    similar.append(similar_obj)

        with transaction.atomic():
            created_materials = Material.objects.bulk_create(materials)
            SimilarMaterialToRequest.objects.bulk_create(similar)

        materials.extend(created_materials)
