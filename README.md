
1. Apply CRD

kubectl apply -f postgres-crd.yaml

2. Apply CRD Object

kubectl apply -f postgres-obj.yaml

3. Run Operator

kopf run run.py 
