from rest_framework import serializers


class LogicalDeleteModelSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ('date_removed', 'created_at', 'updated_at')
        fields = ('date_removed', 'created_at', 'updated_at')

    def get_extra_kwargs(self):
        extra_kwargs = super(LogicalDeleteModelSerializer, self).get_extra_kwargs()

        read_only_fields = getattr(super(self.__class__, self).Meta, 'read_only_fields', None)
        if read_only_fields is not None:
            for field_name in read_only_fields:
                kwargs = extra_kwargs.get(field_name, {})
                kwargs['read_only'] = True
                extra_kwargs[field_name] = kwargs
        return extra_kwargs

    def get_field_names(self, declared_fields, info):
        fields = super(LogicalDeleteModelSerializer, self).get_field_names(declared_fields, info)
        if isinstance(fields, tuple):
            return fields + (getattr(super(self.__class__, self).Meta, 'fields'))
        else:
            return fields

