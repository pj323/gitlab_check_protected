# Team Turing Distributed Caching Service Architecture

## Overview

This architecture diagram illustrates a Container-as-a-Service (CaaS) namespace setup for a distributed caching service managed by Team Turing. It involves various components like load balancers, Redis for caching, Prometheus and Grafana for monitoring, and Tiller for deployment automation. Below is a detailed breakdown of each component and their interactions.

![Architecture Diagram](path_to_your_architecture_diagram_image)

## Components Breakdown

### Load Balancer
- **Function:** Distributes incoming application traffic across multiple pods to ensure no single pod is overwhelmed.
- **Flow:** Receives application flow from TP 2 (presumably a traffic provider or client) and forwards it to the appropriate pod via Cluster IP.

### Cluster IP
- **Function:** Acts as a virtual IP to load balance the traffic to the service pods within the cluster.
- **Flow:** Receives traffic from the Load Balancer and directs it to the appropriate pod based on the service discovery mechanism.

### Ingress
- **Function:** Manages external access to the services in the cluster, typically through HTTP and HTTPS.
- **Flow:** Handles HTTP traffic to and from the Redis Engineer, allowing for external management and monitoring.

### Redis
- **Components:**
  - **Redis v5.x:** The primary caching layer.
  - **Redis Metrics Exporter:** Exports Redis metrics to Prometheus for monitoring.
- **Flow:** Receives application flow and interacts with Prometheus to export metrics.

### Prometheus
- **Version:** v2.4.3
- **Function:** Collects and stores metrics from various components for monitoring and alerting.
- **Flow:** Collects metrics from Redis and its metrics exporter and forwards alert data to Alert Manager.

### Grafana
- **Version:** v5.4.3
- **Function:** Visualizes the data collected by Prometheus.
- **Flow:** Receives HTTP traffic from Prometheus and displays it in a user-friendly dashboard for monitoring.

### Alert Manager
- **Version:** v0.16.1
- **Function:** Manages alerts sent by Prometheus, including deduplication, grouping, and routing.
- **Flow:** Receives alert data from Prometheus and manages alert notifications.

### Tiller
- **Version:** v2.11.0
- **Function:** Manages Helm package deployments within the Kubernetes cluster.
- **Flow:** Interacts with the CaaS API for deployment automation and manages the deployment of various components like Redis, Prometheus, Grafana, and Alert Manager.

### CaaS API
- **Function:** Provides an interface for managing the deployment and scaling of containerized applications.
- **Flow:** Facilitates management and automation interactions, particularly with the Redis Engineer for HTTP traffic and management tasks.

### Storage (PVC)
- **Components:**
  - **AlertManager Persistent Volume**
  - **Grafana Persistent Volume**
  - **Prometheus Persistent Volume**
  - **Redis Persistent Volume**
- **Function:** Provides persistent storage for the stateful components to retain data across pod restarts and rescheduling.

## Interaction Flows

### Application Flow
- Begins from TP 2, passes through the Load Balancer, and is distributed to the appropriate services via Cluster IP.
- Redis processes the application data and interacts with Prometheus for metrics collection.

### Prometheus Flow
- Collects metrics from Redis and its exporter, forwarding this data to Alert Manager for alert processing.
- Sends HTTP traffic to Grafana for data visualization.

### Alert Manager Flow
- Manages alerts received from Prometheus, ensuring that alerts are appropriately routed and managed.

### Management and Automation
- Redis Engineer interacts with the CaaS API for management tasks, facilitated by Ingress for HTTP traffic.
- Tiller manages deployment automation by interacting with the CaaS API and deploying the necessary components to their respective persistent volumes.

## Example Scenario: User Login with Session Caching

Let's consider a practical example where this system is used to manage user login sessions for a web application.

### User Login Request
- A user attempts to log in to the web application, sending a login request to the application server.

### Routing to Redis
- The application server sends this request through the Load Balancer, which directs it to one of the Redis instances via the Cluster IP.

### Session Management in Redis
- Redis checks if the user's session already exists. If not, it creates a new session entry and stores the user's session data, such as user ID, authentication token, and session expiration time.
- The session data is stored in-memory for quick access.

### Metrics Collection
- Redis Metrics Exporter collects metrics related to this transaction, such as request count, response time, and memory usage, and exports these to Prometheus.

### Monitoring and Alerts
- Prometheus continuously monitors Redis metrics. If any metric exceeds predefined thresholds (e.g., high memory usage or slow response time), it sends an alert to the Alert Manager.
- The Alert Manager processes and routes this alert to the appropriate channels (e.g., notifying the Redis Engineer via email or a messaging platform).

### Dashboard Visualization
- Grafana visualizes the metrics collected by Prometheus, displaying them on a dashboard. Engineers can see real-time data on login requests, Redis performance, and any active alerts.

### External Management
- The Redis Engineer can access the system through the Ingress, using the CaaS API for management tasks such as scaling Redis instances or updating configurations.
- Tiller automates deployment and scaling processes, ensuring that the Redis service adapts to changing loads.


# Team Turing Network Architecture

## Overview

This network architecture diagram illustrates the networking components and their interactions within the distributed caching service managed by Team Turing. It includes components like PCF, BGP, Switch Pairs, MetalLB, and Kubernetes Workers. Below is a detailed breakdown of each component and their interactions.

![Networking Architecture Diagram](path_to_your_network_architecture_diagram_image)

## Components Breakdown

### PCF (Pivotal Cloud Foundry)
- **Components:**
  - **Diego:** The container orchestration system used by PCF.
  - **Req/Resp App:** Applications running on PCF that send requests and receive responses.
- **Flow:** 
  - Applications send requests through Diego, which are then routed to the appropriate destination.
  - Responses are routed back to the applications via Diego.

### IP Core
- **Function:** Acts as the central routing and switching point for the network traffic.
- **Flow:** Connects the PCF components to the BGP and Switch Pairs, ensuring proper routing of network traffic.

### BGP (Border Gateway Protocol)
- **Components:**
  - **Quagga Instances (0 to 3):** BGP daemons that manage the routing information.
- **Flow:** 
  - Quagga instances handle the distribution of routing information between different network segments.
  - They interact with the IP Core and Switch Pairs to ensure efficient routing.

### Switch Pairs
- **Function:** Provide redundant switching paths to ensure high availability and fault tolerance.
- **Components:**
  - **Switch Pair 1**
  - **Switch Pair 2**
- **Flow:** 
  - Network traffic is routed through these switches to ensure redundancy and load balancing.
  - They connect the BGP components to the Kubernetes workers.

### MetalLB (Load Balancer for Kubernetes)
- **Function:** Provides network load balancing for Kubernetes clusters.
- **Flow:** 
  - Receives traffic from the Switch Pairs and distributes it across the Kubernetes Worker nodes.
  - Ensures that the traffic is balanced and routed to the appropriate Redis pods.

### Kubernetes Workers
- **Components:**
  - **K8s Worker Nodes:** Nodes in the Kubernetes cluster that run the application pods.
  - **Redis Pods:** Pods running Redis instances for the distributed caching service.
- **Flow:** 
  - MetalLB directs traffic to the appropriate Kubernetes Worker node.
  - The Worker node routes the traffic to the corresponding Redis pod, which handles the request and processes the data.

## Interaction Flows

### Application Request Flow
1. **Request Initiation:**
   - An application running on PCF sends a request through Diego.
   
2. **Routing via IP Core:**
   - The request is routed through the IP Core to the appropriate BGP instance.

3. **BGP Routing:**
   - Quagga instances within BGP handle the routing information and direct the request to the appropriate Switch Pair.

4. **Switching and Load Balancing:**
   - Switch Pairs ensure redundancy and load balance the request, routing it towards the Kubernetes Worker nodes.

5. **Load Balancing with MetalLB:**
   - MetalLB receives the request from the Switch Pairs and distributes it to the appropriate Kubernetes Worker node.

6. **Processing in Kubernetes:**
   - The Kubernetes Worker node routes the request to the appropriate Redis pod.
   - The Redis pod processes the request and returns the response.

### Example Scenario: Data Retrieval from Redis Cache

Let's consider a practical example where an application retrieves data from the Redis cache.

1. **Data Request:**
   - An application running on PCF sends a data retrieval request to the Redis cache.

2. **Request Routing:**
   - The request is routed through Diego to the IP Core.
   - The IP Core directs the request to a Quagga instance in the BGP.

3. **BGP Routing:**
   - The Quagga instance processes the routing information and forwards the request to a Switch Pair.

4. **Switch Pair Handling:**
   - The Switch Pair ensures the request is balanced and routes it towards MetalLB.

5. **Load Balancing:**
   - MetalLB distributes the request to the appropriate Kubernetes Worker node.

6. **Redis Pod Processing:**
   - The Kubernetes Worker node routes the request to the corresponding Redis pod.
   - The Redis pod retrieves the requested data from the cache and sends the response back.

7. **Response Routing:**
   - The response follows the reverse path, going from the Redis pod to the Kubernetes Worker node, through MetalLB, the Switch Pair, BGP, IP Core, and finally back to the application via Diego.

## Conclusion

This example demonstrates how the network architecture handles a data retrieval request, ensuring efficient routing, load balancing, and high availability. The architecture supports scalability, fault tolerance, and robust management, making it well-suited for demanding web applications requiring efficient networking solutions.


## Conclusion

This example demonstrates how the distributed caching service handles user login requests, manages session data, and ensures system performance and reliability through continuous monitoring and alerting. The architecture supports scalability, high availability, and robust management, making it well-suited for demanding web applications requiring efficient caching solutions.
