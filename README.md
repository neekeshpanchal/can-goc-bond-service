
### Local Kubernetes Deployment of a Bond Pricing API
Fully containerized API running in a local Kubernetes cluster, accessible externally, and ready for scaling.

* **Python API Development**

  * Built a bond pricing API (zero-coupon and coupon bonds) with Flask.
  * Tested API functionality with direct HTTP requests.

* **Containerization**

  * Created a Docker image using Gunicorn as the WSGI server.
  * Verified container runs independently.

* **Kubernetes Deployment (Minikube)**

  * Set up a local Minikube cluster.
  * Deployed API via a Deployment with multiple replicas.
  * Exposed pods internally using a ClusterIP Service.

* **Ingress and Routing**

  * Configured NGINX Ingress for external access (`can-gov-bonds.local`).
  * Updated hosts file for local DNS resolution.
  * Verified external API access through Ingress.

* **Scaling and High Availability**

  * Explored Horizontal Pod Autoscaler for CPU-based scaling.
  * Ensured multiple pods handle load for service availability.
<img width="939" height="334" alt="image" src="https://github.com/user-attachments/assets/adfc1f51-0294-4a40-830f-2869583ad454" />


