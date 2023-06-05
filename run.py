import kopf
from kubernetes import client, config
import asyncio

config.load_kube_config()

@kopf.on.create('postgres.example.com', 'v1', 'postgresdatabases')
def create_postgres_database(body, **kwargs):
    api = client.ApiClient()
    core_v1_api = client.CoreV1Api(api)
    app_v1_api = client.AppsV1Api(api)

    # Retrieve the relevant information from the custom resource
    namespace = body['metadata']['namespace']
    name = body['metadata']['name']
    password = body['spec']['password']

    # Create a Deployment for the PostgreSQL database
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

    app_v1_api.create_namespaced_deployment(namespace, deployment)

    # Create a Service for the PostgreSQL database
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

    core_v1_api.create_namespaced_service(namespace, service)

@kopf.on.delete('postgres.example.com', 'v1', 'postgresdatabases')
def delete_postgres_database(body, **kwargs):
    api = client.Api

# @kopf.on.timer('postgres.example.com', 'v1', 'postgresdatabases')
# def scan_postgres_database(body, **kwargs):
#     api = client.Api
