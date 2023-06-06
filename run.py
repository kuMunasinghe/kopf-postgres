from venv import logger
import kopf
from kubernetes import client, config
import asyncio

config.load_kube_config()

@kopf.on.create('postgres.example.com', 'v1', 'postgresdatabases')
def create_postgres_database(body, **kwargs):
    api = client.ApiClient()
    core_v1_api = client.CoreV1Api(api)
    app_v1_api = client.AppsV1Api(api)

    namespace = body['metadata']['namespace']
    name = body['metadata']['name']
    password = body['spec']['password']
    input =body['spec']['input']

    deployment = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': name,
            'namespace': namespace
        },
        'spec': {
            'replicas': 1,
            'selector': {
                'matchLabels': {
                    'app': name
                }
            },
            'template': {
                'metadata': {
                    'labels': {
                        'app': name
                    }
                },
                'spec': {
                    'containers': [
                        {
                            'name': 'postgres',
                            'image': 'postgres:latest',
                            'env': [
                                {
                                    'name': 'POSTGRES_PASSWORD',
                                    'value': password
                                }
                            ],
                            'ports': [
                                {
                                    'containerPort': 5432
                                }
                            ],
                            'volumeMounts': [
                                {
                                    'name': 'pgdata',
                                    'mountPath': '/var/lib/postgresql/data'
                                }
                            ]
                        }
                    ],
                    'volumes': [
                        {
                            'name': 'pgdata',
                            'emptyDir': {}
                        }
                    ]
                }
            }
        }
    }

    # app_v1_api.create_namespaced_deployment(namespace, deployment)
    try:
        app_v1_api.create_namespaced_deployment(namespace, deployment)
    except client.exceptions.ApiException as e:
        if e.status == 409:
            logger.warning(f"Deployment '{name}' already exists.")
        else:
            # Handle other types of exceptions
            logger.error(f"Failed to create deployment '{name}': {e}")
            return
        
    service = {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {
            'name': name,
            'namespace': namespace
        },
        'spec': {
            'selector': {
                'app': name
            },
            'ports': [
                {
                    'protocol': 'TCP',
                    'port': 5432,
                    'targetPort': 5432
                }
            ]
        }
    }

    try:
        core_v1_api.create_namespaced_service(namespace, service)
    except client.exceptions.ApiException as e:
        if e.status == 409:
            logger.warning(f"Service '{name}' already exists.")
        else:
            # Handle other types of exceptions
            logger.error(f"Failed to create service '{name}': {e}")
            return
    logger.info(f"input in crd object: '{input}'")
    # return(str(input))
    


@kopf.on.delete('postgres.example.com', 'v1', 'postgresdatabases')
def delete_postgres_database(body, **kwargs):
    api = client.Api

# @kopf.on.timer('postgres.example.com', 'v1', 'postgresdatabases')
# def scan_postgres_database(body, **kwargs):
#     api = client.Api

@kopf.on.update('postgres.example.com', 'v1', 'postgresdatabases')
def create_postgres_database(body, **kwargs):
    api = client.ApiClient()
    core_v1_api = client.CoreV1Api(api)
    app_v1_api = client.AppsV1Api(api)

    namespace = body['metadata']['namespace']
    name = body['metadata']['name']
    password = body['spec']['password']
    input =body['spec']['input']

    deployment = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': name,
            'namespace': namespace
        },
        'spec': {
            'replicas': 1,
            'selector': {
                'matchLabels': {
                    'app': name
                }
            },
            'template': {
                'metadata': {
                    'labels': {
                        'app': name
                    }
                },
                'spec': {
                    'containers': [
                        {
                            'name': 'postgres',
                            'image': 'postgres:latest',
                            'env': [
                                {
                                    'name': 'POSTGRES_PASSWORD',
                                    'value': password
                                }
                            ],
                            'ports': [
                                {
                                    'containerPort': 5432
                                }
                            ],
                            'volumeMounts': [
                                {
                                    'name': 'pgdata',
                                    'mountPath': '/var/lib/postgresql/data'
                                }
                            ]
                        }
                    ],
                    'volumes': [
                        {
                            'name': 'pgdata',
                            'emptyDir': {}
                        }
                    ]
                }
            }
        }
    }

    # app_v1_api.create_namespaced_deployment(namespace, deployment)
    try:
        app_v1_api.create_namespaced_deployment(namespace, deployment)
    except client.exceptions.ApiException as e:
        if e.status == 409:
            logger.warning(f"Deployment '{name}' already exists.")
        else:
            # Handle other types of exceptions
            logger.error(f"Failed to create deployment '{name}': {e}")
            return
        
    service = {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {
            'name': name,
            'namespace': namespace
        },
        'spec': {
            'selector': {
                'app': name
            },
            'ports': [
                {
                    'protocol': 'TCP',
                    'port': 5432,
                    'targetPort': 5432
                }
            ]
        }
    }

    try:
        core_v1_api.create_namespaced_service(namespace, service)
    except client.exceptions.ApiException as e:
        if e.status == 409:
            logger.warning(f"Service '{name}' already exists.")
        else:
            # Handle other types of exceptions
            logger.error(f"Failed to create service '{name}': {e}")
            return
    logger.info(f"input in crd object: '{input}'")
    # return(str(input))
    

