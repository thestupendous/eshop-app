#ensure that kubernetes is installed

kubectl apply -f ns.yaml && \
kubectl apply -f pv.yaml && \
kubectl apply -f pvc.yaml && \
kubectl apply -f mongo-deployment.yaml && \
kubectl apply -f backend-service.yaml && \
kubectl apply -f frontend-deployment.yaml && \
kubectl apply -f frontend-service.yaml