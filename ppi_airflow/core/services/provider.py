from ppi_airflow.core.services.factory import ServiceFactory


class ServiceProvider(ServiceFactory):
    def get(self, service_name, **kwargs):
        return self.create(service_name, **kwargs)
