Here's an improved README for your project, with detailed instructions for setting up Docker and Kubernetes:

# Container Scaling with RabbitMQ, Docker, Kubernetes, and Keda

This tutorial demonstrates the use of RabbitMQ, Docker, Kubernetes, and Keda to manage container scaling based on message traffic. Eventually, we will replace RabbitMQ with another messaging library, like Google Cloud Pub/Sub.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Setup](#setup)
   - [Docker Setup](#docker-setup)
   - [Kubernetes Setup](#kubernetes-setup)
4. [Usage](#usage)
5. [Switching to Google Cloud Pub/Sub](#switching-to-google-cloud-pubsub)
6. [Contributing](#contributing)
7. [License](#license)
8. [Author](#Me)

## Prerequisites

Before starting, ensure you have the following installed on your system:

- Docker
- Kubernetes (kubectl and minikube)
- Docker Compose
- Python 3.9+
- pip

## Project Structure

```plaintext
.
├── function_a
│   ├── Dockerfile
│   └── ...
├── function_b
│   ├── Dockerfile
│   └── ...
├── rest_api
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── rest_main.py
│   └── ...
├── rpc_api
│   ├── Dockerfile
│   └── ...
├── docker-compose.yaml
└── README.md
```

## Setup

### Docker Setup

1. **Build the Docker images:**

   Navigate to the project root directory and run the following command:

   ```bash
   docker-compose build
   ```

2. **Start the services:**

   Run the following command to start all the services defined in the `docker-compose.yaml` file:

   ```bash
   docker-compose up
   ```

3. **Verify the services are running:**

   You can check the status of the services using:

   ```bash
   docker-compose ps
   ```

   To access logs for a specific service:

   ```bash
   docker-compose logs <service_name>
   ```

### Kubernetes Setup

1. **Start Minikube:**

   If you don't have a Kubernetes cluster, you can use Minikube to create one locally:

   ```bash
   minikube start
   ```

2. **Deploy RabbitMQ:**

   Apply the RabbitMQ deployment configuration:

   ```bash
   kubectl apply -f https://k8s.io/examples/application/rabbitmq/rabbitmq-statefulset.yaml
   ```

3. **Build and push Docker images to a registry:**

   Minikube uses its own Docker daemon, so you need to build images inside Minikube's environment:

   ```bash
   eval $(minikube docker-env)
   docker-compose build
   ```

4. **Deploy your services:**

   Create Kubernetes deployment and service YAML files for your services. Example for `rest_api`:

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: restapi
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: restapi
     template:
       metadata:
         labels:
           app: restapi
       spec:
         containers:
         - name: restapi
           image: restapi:latest
           ports:
           - containerPort: 8000
           volumeMounts:
           - mountPath: /var/run/docker.sock
             name: docker-sock
         volumes:
         - name: docker-sock
           hostPath:
             path: /var/run/docker.sock
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: restapi-service
   spec:
     selector:
       app: restapi
     ports:
       - protocol: TCP
         port: 8000
         targetPort: 8000
   ```

   Apply the deployment:

   ```bash
   kubectl apply -f restapi-deployment.yaml
   ```

5. **Install Keda:**

   Follow the Keda installation guide from their [official documentation](https://keda.sh/docs/2.0/deploy/).

6. **Create Keda ScaledObject:**

   Define a `ScaledObject` for your RabbitMQ consumer service. Example:

   ```yaml
   apiVersion: keda.sh/v1alpha1
   kind: ScaledObject
   metadata:
     name: rabbitmq-scaledobject
   spec:
     scaleTargetRef:
       name: rpc-api
     triggers:
     - type: rabbitmq
       metadata:
         host: amqp://guest:guest@rabbitmq
         queueName: your-queue-name
         queueLength: "10"
   ```

   Apply the `ScaledObject`:

   ```bash
   kubectl apply -f scaledobject.yaml
   ```

## Usage

Once your services are up and running, you can interact with them via their exposed endpoints. Check your service definitions for the specific ports and routes.

## Switching to Google Cloud Pub/Sub

To replace RabbitMQ with Google Cloud Pub/Sub, follow these steps:

1. **Install Google Cloud SDK and authenticate:**

   ```bash
   gcloud init
   ```

2. **Modify your services to use Pub/Sub:**

   Update the code in your services to publish and consume messages from Google Cloud Pub/Sub instead of RabbitMQ.

3. **Update Dockerfiles and Kubernetes deployments:**

   Ensure your Docker images include necessary dependencies for Google Cloud Pub/Sub, and update Kubernetes manifests accordingly.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Me
**Alfred Nana Brown** 

**Let's connect on** 

  [<img src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/linkedin.svg" alt="LinkedIn" height="20" width="20">](https://www.linkedin.com/in/alfred-nana-brown/) 
  [<img src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/twitter.svg" alt="Twitter" height="20" width="20">](https://x.com/AgyirBrown) 
  [<img src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/gmail.svg" alt="Gmail" height="20" width="20">](mailto:nanabrown.agyir@gmail.com) 
  [<img src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/github.svg" alt="GitHub" height="20" width="20">](https://github.com/NanaAgyirBrown) 
  [<img src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/medium.svg" alt="Medium" height="20" width="20">](https://medium.com/@nanabrown.agyir)
