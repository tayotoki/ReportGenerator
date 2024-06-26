from crm.loaders import BaseLoader


class RequestStatsLoader(BaseLoader):
    def load_data_from_crm(self):
        for table in self.client.get_tables(
            names=list(self.converter.FIELDS_MAPPER.values()),
        ):
            raw_data = table.to_dict(orient="records")
            requests_to_create = []
            requests_co_update = {}

            request_numbers = set(self.model.objects.all().values_list("number", flat=True))

            for data in raw_data:
                if (number := data[self.converter.FIELDS_MAPPER["number"]]) in request_numbers:
                    requests_co_update[number] = dict(**self.converter(data=data))
                else:
                    requests_to_create.append(self.model(**self.converter(data=data)))
            self.bulk_create(instances=requests_to_create)
            self.bulk_update(instances_data=requests_co_update)

    def bulk_update(self, instances_data: dict[str, dict]):
        super().bulk_update(instances_data=instances_data)

        if instances_data:
            update_instances = self.model._base_manager.filter(number__in=instances_data)
            for instance in update_instances:
                for field_name, field_value in instances_data[instance.number].items():
                    setattr(instance, field_name, field_value)

            self.model._base_manager.bulk_update(update_instances, fields=self.converter.UPDATE_FIELDS)

            self.count_updated_objects = len(instances_data)
