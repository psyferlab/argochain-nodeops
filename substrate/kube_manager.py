import subprocess
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def run_command(command):
    """Execute a kubectl command and handle output."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        console.print("[green]Command executed successfully![/]", justify="center")
        console.print(result.stdout)
    except subprocess.CalledProcessError as e:
        console.print("[red]Error executing command:[/]", justify="center")
        console.print(e.stderr)

def show_menu():
    """Display the options menu."""
    table = Table(title="Kubernetes Management CLI", show_header=True, header_style="bold magenta")
    table.add_column("Option", style="dim", width=12)
    table.add_column("Action", min_width=20)
    table.add_row("1", "Create Standard Deployment")
    table.add_row("2", "Create Deployment with Persistent Volume")
    table.add_row("3", "Create Deployment with Environment Variables")
    table.add_row("4", "Delete Deployment")
    table.add_row("5", "List Pods")
    table.add_row("6", "Create Service")
    table.add_row("7", "Delete Service")
    table.add_row("8", "Scale Deployment")
    table.add_row("9", "Update Deployment Image")
    table.add_row("10", "View Pod Logs")
    table.add_row("11", "Restart Deployment")
    table.add_row("12", "Set Resource Limits")
    table.add_row("13", "Set Up Basic Monitoring")
    table.add_row("14", "Configure Alerts")
    table.add_row("15", "Exit")
    console.print(table)

def create_deployment():
    name = Prompt.ask("Enter Deployment Name")
    image = Prompt.ask("Enter Image (e.g., nginx:latest)")
    replicas = Prompt.ask("Enter Number of Replicas", default="1")
    command = f"kubectl create deployment {name} --image={image} --replicas={replicas}"
    run_command(command)

def create_deployment_with_pv():
    name = Prompt.ask("Enter Deployment Name")
    image = Prompt.ask("Enter Image")
    pvc_name = Prompt.ask("Enter PVC Name")
    command = f"kubectl run {name} --image={image} --replicas=1 --dry-run=client -o yaml | kubectl set volume --name={name}-volume --type=persistentVolumeClaim --claim-name={pvc_name} --mount-path=/path/in/container > {name}.yaml && kubectl apply -f {name}.yaml"
    run_command(command)

def create_deployment_with_env():
    name = Prompt.ask("Enter Deployment Name")
    image = Prompt.ask("Enter Image")
    key = Prompt.ask("Enter Environment Variable Key")
    value = Prompt.ask("Enter Environment Variable Value")
    command = f"kubectl run {name} --image={image} --env {key}={value} --replicas=1 --dry-run=client -o yaml > {name}.yaml && kubectl apply -f {name}.yaml"
    run_command(command)

def delete_deployment():
    name = Prompt.ask("Enter Deployment Name to Delete")
    command = f"kubectl delete deployment {name}"
    run_command(command)

def list_pods():
    command = "kubectl get pods"
    run_command(command)

def create_service():
    name = Prompt.ask("Enter Deployment Name to Expose")
    type_choice = Prompt.choose("Choose Service Type", choices=["ClusterIP", "NodePort", "LoadBalancer"])
    port = Prompt.ask("Enter Service Port")
    command = f"kubectl expose deployment {name} --type={type_choice} --port={port}"
    run_command(command)

def delete_service():
    name = Prompt.ask("Enter Service Name to Delete")
    command = f"kubectl delete service {name}"
    run_command(command)

def scale_deployment():
    name = Prompt.ask("Enter Deployment Name to Scale")
    replicas = Prompt.ask("Enter New Number of Replicas")
    command = f"kubectl scale deployment {name} --replicas={replicas}"
    run_command(command)

def update_deployment_image():
    name = Prompt.ask("Enter Deployment Name")
    image = Prompt.ask("Enter New Image (e.g., nginx:latest)")
    command = f"kubectl set image deployment/{name} *=${image}"
    run_command(command)

def view_pod_logs():
    pod_name = Prompt.ask("Enter Pod Name")
    command = f"kubectl log{pod_name}"
    run_command(command)

def restart_deployment():
    name = Prompt.ask("Enter Deployment Name to Restart")
    command = f"kubectl rollout restart deployment/{name}"
    run_command(command)

def set_resource_limits():
    name = Prompt.ask("Enter Deployment Name")
    cpu = Prompt.ask("Enter CPU limit (e.g., 500m for 0.5 cores)")
    memory = Prompt.ask("Enter Memory limit (e.g., 1Gi)")
    command = f"kubectl set resources deployment/{name} --limits=cpu={cpu},memory={memory}"
    run_command(command)

def setup_basic_monitoring():
    command = "kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml"
    run_command(command)

def configure_alerts():
    command = "kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/master/bundle.yaml"
    run_command(command)

def main():
    actions = {
        '1': create_deployment,
        '2': create_deployment_with_pv,
        '3': create_deployment_with_env,
        '4': delete_deployment,
        '5': list_pods,
        '6': create_service,
        '7': delete_service,
        '8': scale_deployment,
        '9': update_deployment_image,
        '10': view_pod_logs,
        '11': restart_deployment,
        '12': set_resource_limits,
        '13': setup_basic_monitoring,
        '14': configure_alerts,
        '15': exit
    }

    while True:
        show_menu()
        choice = Prompt.ask("Choose an option", choices=[str(i) for i in range(1, 16)])
        action = actions.get(choice)
        if action:
            action()

if __name__ == '__main__':
    main()