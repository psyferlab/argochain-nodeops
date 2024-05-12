#!/bin/bash

# Function to execute kubectl commands and handle output
function kubectl_command() {
    command=$1
    echo "Executing: $command"
    eval $command
    if [ $? -ne 0 ]; then
        echo "Error executing command: $command"
    else
        echo "Command executed successfully: $command"
    fi
}

# Display options menu
function show_menu() {
    echo "Kubernetes Kickstarter CLI - Choose an option:"
    echo "1.  Create Standard Deployment"
    echo "2.  Create Deployment with Persistent Volume"
    echo "3.  Create Deployment with Environment Variables"
    echo "4.  Delete Deployment"
    echo "5.  List Pods"
    echo "6.  Create Service"
    echo "7.  Delete Service"
    echo "8.  Scale Deployment"
    echo "9.  Update Deployment Image"
    echo "10. View Pod Logs"
    echo "11. Restart Deployment"
    echo "12. Set Resource Limits"
    echo "13. Set Up Basic Monitoring"
    echo "14. Configure Alerts"
    echo "15. Exit"
}

# Run the selected action
function run_selected_action() {
    read -p "Enter your choice: " choice
    case $choice in
        1) create_deployment;;
        2) create_deployment_with_pv;;
        3) create_deployment_with_env;;
        4) delete_deployment;;
        5) list_pods;;
        6) create_service;;
        7) delete_service;;
        8) scale_deployment;;
        9) update_deployment_image;;
        10) view_pod_logs;;
        11) restart_deployment;;
        12) set_resource_limits;;
        13) setup_basic_monitoring;;
        14) configure_alerts;;
        15) exit 0;;
        *) echo "Invalid option selected. Exiting."; exit 1;;
    esac
}

# Define functions for each action

function create_deployment() {
    read -p "Enter Deployment Name: " name
    read -p "Enter Image (e.g., nginx:latest): " image
    read -p "Enter Number of Replicas: " replicas
    kubectl_command "kubectl create deployment $name --image=$image --replicas=$replicas"
}

function create_deployment_with_pv() {
    read -p "Enter Deployment Name: " name
    read -p "Enter Image: " image
    read -p "Enter PVC Name: " pvc_name
    kubectl_command "kubectl run $name --image=$image --replicas=1 --dry-run=client -o yaml | kubectl set volume --name=$name-volume --type=persistentVolumeClaim --claim-name=$pvc_name --mount-path=/path/in/container > $name.yaml && kubectl apply -f $name.yaml"
}

function create_deployment_with_env() {
    read -p "Enter Deployment Name: " name
    read -p "Enter Image: " image
    read -p "Enter Environment Variable Key: " key
    read -p "Enter Environment Variable Value: " value
    kubectl_command "kubectl run $name --image=$image --env $key=$value --replicas=1 --dry-run=client -o yaml > $name.yaml && kubectl apply -f $name.yaml"
}

function delete_deployment() {
    read -p "Enter Deployment Name to Delete: " name
    kubectl_command "kubectl delete deployment $name"
}

function list_pods() {
    kubectl_command "kubectl get pods"
}

function create_service() {
    read -p "Enter Deployment Name to Expose: " name
    echo "Select Service Type:"
    echo "1. ClusterIP - Default, internal network only."
    echo "2. NodePort - Exposes the service on each Node’s IP at a static port."
    echo "3. LoadBalancer - Exposes the service externally using a cloud provider’s load balancer."
    read -p "Enter choice: " type_choice
    case $type_choice in
        1) type="ClusterIP";;
        2) type="NodePort";;
        3) type="LoadBalancer";;
        *) echo "Invalid choice"; exit 1;;
    esac
    read -p "Enter Service Port: " port
    kubectl_command "kubectl expose deployment $name --type=$type --port=$port"
}

function delete_service
() {
    read -p "Enter Service Name to Delete: " name
    kubectl_command "kubectl delete service $name"
}

function scale_deployment() {
    read -p "Enter Deployment Name to Scale: " name
    read -p "Enter New Number of Replicas: " replicas
    kubectl_command "kubectl scale deployment $name --replicas=$replicas"
}

function update_deployment_image() {
    read -p "Enter Deployment Name: " name
    read -p "Enter New Image (e.g., nginx:latest): " image
    kubectl_command "kubectl set image deployment/$name *=${image}"
}

function view_pod_logs() {
    read -p "Enter Pod Name: " pod_name
    kubectl_command "kubectl logs $pod_name"
}

function restart_deployment() {
    read -p "Enter Deployment Name to Restart: " name
    kubectl_command "kubectl rollout restart deployment/$name"
}

function set_resource_limits() {
    read -p "Enter Deployment Name: " name
    read -p "Enter CPU limit (e.g., 500m for 0.5 cores): " cpu
    read -p "Enter Memory limit (e.g., 1Gi): " memory
    kubectl_command "kubectl set resources deployment $name --limits=cpu=$cpu,memory=$memory"
}

function setup_basic_monitoring() {
    kubectl_command "kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml"
}

function configure_alerts() {
    kubectl_command "kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/master/bundle.yaml"
}

# Main loop to show the menu and get user actions
while true; do
    show_menu
    run_selected_action
done
```