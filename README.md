### Local Kubernetes Deployment of a Bond Pricing API
Fully containerized API running in a local Kubernetes cluster.

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

# **Bond Pricing API – `/price` Endpoint**

**URL:**

```
POST /price
```

**Description:**
Calculate the price of a bond (zero-coupon or fixed-coupon) using an interpolated yield curve. You can optionally provide a custom yield curve or use the default curve.

---

## **Request JSON Parameters**

| Parameter          | Type   | Required                        | Default            | Description                                                                                                                                                                 |
| ------------------ | ------ | ------------------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`             | string | No                              | `"zero"`           | Type of bond. `"zero"` = zero-coupon bond, `"coupon"` = fixed-coupon bond.                                                                                                  |
| `maturity_years`   | float  | Yes                             | N/A                | Time to maturity in years. Can be fractional (e.g., 7.5).                                                                                                                   |
| `face`             | float  | No                              | 1000.0             | Face (par) value of the bond.                                                                                                                                               |
| `coupon_rate`      | float  | Required if `type` = `"coupon"` | N/A                | Annual coupon rate in decimal form (e.g., 0.025 = 2.5%). Ignored for zero-coupon bonds.                                                                                     |
| `coupons_per_year` | int    | No                              | 1                  | Number of coupon payments per year. Only relevant for `"coupon"` bonds.                                                                                                     |
| `curve`            | object | No                              | Uses default curve | Optional custom yield curve. Keys = tenor buckets, values = annual spot rates in decimals. Must include all buckets: `"1-3Y"`, `"3-5Y"`, `"5-10Y"`, `"10-15Y"`, `"15-30Y"`. |

---

## **Default Yield Curve**

If no `curve` is provided, the API uses the following default:

```json
{
  "1-3Y": 0.015,
  "3-5Y": 0.018,
  "5-10Y": 0.020,
  "10-15Y": 0.025,
  "15-30Y": 0.030
}
```

---

## **Example Requests**

### **1. Zero-coupon bond using default curve**

```bash
curl -X POST http://can-gov-bonds.local/price \
     -H "Content-Type: application/json" \
     -d '{
           "type": "zero",
           "maturity_years": 5,
           "face": 1000
         }'
```

---

### **2. Fixed-coupon bond using default curve**

```bash
curl -X POST http://can-gov-bonds.local/price \
     -H "Content-Type: application/json" \
     -d '{
           "type": "coupon",
           "maturity_years": 10,
           "face": 1000,
           "coupon_rate": 0.02,
           "coupons_per_year": 2
         }'
```

---

### **3. Bond with custom yield curve**

```bash
curl -X POST http://can-gov-bonds.local/price \
     -H "Content-Type: application/json" \
     -d '{
           "type": "zero",
           "maturity_years": 7,
           "face": 1000,
           "curve": {
               "1-3Y": 0.012,
               "3-5Y": 0.017,
               "5-10Y": 0.022,
               "10-15Y": 0.027,
               "15-30Y": 0.032
           }
         }'
```

---

## **Response JSON**

| Field            | Type   | Description                         |
| ---------------- | ------ | ----------------------------------- |
| `price`          | float  | Calculated bond price.              |
| `maturity_years` | float  | Maturity used for calculation.      |
| `rate_used`      | float  | Spot rate interpolated from curve.  |
| `type`           | string | Bond type (`"zero"` or `"coupon"`). |

**Example Response:**

```json
{
  "price": 905.536,
  "maturity_years": 5,
  "rate_used": 0.018,
  "type": "zero"
}
```
