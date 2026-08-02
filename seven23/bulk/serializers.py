from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ListSerializer


class BulkSerializerMixin:
    def to_internal_value(self, data):
        ret = super().to_internal_value(data)

        id_attr = getattr(self.Meta, 'update_lookup_field', 'id')
        request_method = getattr(
            getattr(self.context.get('view'), 'request', None),
            'method',
            '',
        )

        # Put the lookup field back into validated data for bulk updates;
        # ModelSerializer strips read-only fields such as id by default.
        if all((
            isinstance(self.root, BulkListSerializer),
            id_attr,
            request_method in ('PUT', 'PATCH'),
        )):
            id_field = self.fields[id_attr]
            ret[id_attr] = id_field.get_value(data)

        return ret


class BulkListSerializer(ListSerializer):
    update_lookup_field = 'id'

    def update(self, queryset, all_validated_data):
        id_attr = getattr(self.child.Meta, 'update_lookup_field', 'id')

        all_validated_data_by_id = {
            item.pop(id_attr): item
            for item in all_validated_data
        }

        if not all(
            value and not isinstance(value, type)
            for value in all_validated_data_by_id
        ):
            raise ValidationError('')

        objects_to_update = queryset.filter(**{
            f'{id_attr}__in': all_validated_data_by_id.keys(),
        })

        if len(all_validated_data_by_id) != objects_to_update.count():
            raise ValidationError('Could not find all objects to update.')

        updated_objects = []
        for obj in objects_to_update:
            obj_id = getattr(obj, id_attr)
            updated_objects.append(
                self.child.update(obj, all_validated_data_by_id[obj_id])
            )

        return updated_objects
