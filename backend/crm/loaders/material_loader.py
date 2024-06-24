from crm.loaders import BaseLoader

from materials.models import Material


class MaterialLoader(BaseLoader):
    def load_data_from_crm(self):
        for table in self.client.get_tables(
            names=[
                self.converter.FIELDS_MAPPER.values()
            ]
        ):
            raw_data = table.to_dict(orient="records")
            materials_to_create = []
            materials_to_update = {}

            material_codes = set(self.model.objects.all().values_list("code", flat=True))

            for data in raw_data:
                if data[self.converter.FIELDS_MAPPER["code"]] in material_codes:
                    materials_to_update.update(**self.converter(data=data))
                else:
                    materials_to_create.append(self.converter(data=data))
            self.bulk_create(instances=materials_to_create)
            self.bulk_update(instances_data=materials_to_update)

    def bulk_update(self, instances_data: dict[str, dict]):
        super().bulk_update(instances_data=instances_data)

        if instances_data:
            update_instances = self.model._base_manager.filter(code__in=instances_data)
            for instance in update_instances:
                for field_name, field_value in instances_data[instance.code].items():
                    setattr(instance, field_name, field_value)

            self.model._base_manager.bulk_update(update_instances, fields=self.converter.UPDATE_FIELDS)

            self.count_updated_objects = len(instances_data)
