from collections import OrderedDict

from rest_framework import routers


class CustomRouter(routers.SimpleRouter):

    def get_api_root_view(self, api_urls=None):
        """
        Return a basic root view.
        """
        api_root_dict = OrderedDict()
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        if api_urls:
            for pattern in api_urls:
                api_root_dict[pattern.name] = pattern.name

        return routers.APIRootView.as_view(api_root_dict=api_root_dict)
