# Quiz Application API

## Project Overview
This project is a **Quiz Application API** built using **Flask** for the backend, **MySQL** as the database, and is fully containerized for deployment on **Kubernetes (MicroK8s)**.  

The API supports:  
- User registration and login  
- Quiz creation and management  
- Question and answer handling  
- Automated deployment and teardown of backend and database on a local Kubernetes cluster  

The deployment scripts streamline setting up the backend and database, making it easier to test and manage the application locally.

---

## Project Structure
```
.
├── k8s/                  # Kubernetes manifests (MySQL and backend deployments)
├── api/                  # Flask backend code (endpoints, models, routes)
├── deploy_api.sh         # Deployment script for MicroK8s
├── undeploy.sh           # Cleanup script to remove deployments and services
├── api_test.sh           # Script to run API test cases
└── README.md
```

---

## Local Setup & Deployment

### Steps
1. **Clone the repository**
```bash
git clone <repo-url>
cd <repo-folder>
```

2. **Deploy backend and database**
```bash
sudo ./deploy_api.sh
```
- The script deploys MySQL and the Flask backend
- Wait for all pods to be ready (the script monitors readiness)
- Backend service will be exposed via NodePort, and MySQL is accessible locally

3. **Run API test cases**
```bash
./api_test.sh
```
- Runs automated test cases to verify backend functionality
- Alternatively, use the endpoint format in the script to test custom cases

4. **Code inspection**
```text
Refer to the `api/` folder for all Flask backend source code, including routes, models, and configurations.
```

5. **Cleanup after use**
```bash
./undeploy.sh
```
- Ensures all deployments, services, and resources are removed cleanly from your local Kubernetes cluster

---

## API Endpoints
Example endpoints available after deployment:

| Method | Endpoint               | Description          |
|--------|-----------------------|--------------------|
| POST   | /api/register          | Register a new user |
| POST   | /api/login             | User login          |
| POST   | /api/quiz/create       | Create a new quiz   |
| POST   | /api/question/add      | Add question to quiz|
| POST   | /api/answer/submit     | Submit answer       |

- Accessible locally via **http://127.0.0.1:5001**

---

## Notes
- Deployment scripts assume MicroK8s cluster is running with sufficient resources
- MySQL runs inside the Kubernetes cluster; port-forwarding allows local connections
- Ensure to run `./undeploy.sh` after testing to prevent leftover resources

---


