import argparse
import sys
import subprocess
import openai
from kubernetes import config, client
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_ai_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

def get_namespaces():
    namespaces = api_instance.list_namespace().items
    print("Listing namespaces:")
    for ns in namespaces:
        print(f"- {ns.metadata.name}")

def get_deployments(namespace):
    deployments = apps_v1.list_namespaced_deployment(namespace).items
    print("Listing deployments:")
    for deploy in deployments:
        print(f"- {deploy.metadata.name}")

    # AI insights
    print("\nAI Insights:")
    ai_prompt = f"Provide insights for Kubernetes deployments in namespace {namespace}:"
    ai_response = generate_ai_response(ai_prompt)
    print(ai_response)

def get_pods(namespace):
    pods = api_instance.list_namespaced_pod(namespace).items
    print("Listing pods:")
    for pod in pods:
        print(f"- {pod.metadata.name}")

    # AI insights
    print("\nAI Insights:")
    ai_prompt = f"Provide insights for Kubernetes pods in namespace {namespace}:"
    ai_response = generate_ai_response(ai_prompt)
    print(ai_response)

def get_services(namespace):
    services = api_instance.list_namespaced_service(namespace).items
    print("Listing services:")
    for service in services:
        print(f"- {service.metadata.name}")

    # AI insights
    print("\nAI Insights:")
    ai_prompt = f"Provide insights for Kubernetes services in namespace {namespace}:"
    ai_response = generate_ai_response(ai_prompt)
    print(ai_response)

def get_serviceaccounts(namespace):
    serviceaccounts = api_instance.list_namespaced_service_account(namespace).items
    print("Listing service accounts:")
    for sa in serviceaccounts:
        print(f"- {sa.metadata.name}")

    # AI insights
    print("\nAI Insights:")
    ai_prompt = f"Provide insights for Kubernetes service accounts in namespace {namespace}:"
    ai_response = generate_ai_response(ai_prompt)
    print(ai_response)

def get_statefulsets(namespace):
    statefulsets = apps_v1.list_namespaced_stateful_set(namespace).items
    print("Listing stateful sets:")
    for sts in statefulsets:
        print(f"- {sts.metadata.name}")

    # AI insights
    print("\nAI Insights:")
    ai_prompt = f"Provide insights for Kubernetes stateful sets in namespace {namespace}:"
    ai_response = generate_ai_response(ai_prompt)
    print(ai_response)

config.load_kube_config()

api_instance = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

def run_kubectl_command(args):
    cmd = ["kubectl"] + args
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(result.returncode)

    print(result.stdout.strip())

def create_resource(file=None):
    if file:
        run_kubectl_command(["create", "-f", file])
    else:
        ai_prompt = "What happens when I run the kubectl create command without a file?"
        ai_response = generate_ai_response(ai_prompt)
        print(ai_response)

def delete_resource(resource_type=None, name=None, namespace=None, file=None):
    if file:
        run_kubectl_command(["delete", "-f", file])
    else:
        if not resource_type or not name:
            ai_prompt = "What happens when I run the kubectl delete command without a resource type and name?"
            ai_response = generate_ai_response(ai_prompt)
            print(ai_response)
        else:
            cmd = ["delete", resource_type, name]
            if namespace:
                cmd.extend(["-n", namespace])
            run_kubectl_command(cmd)

def delete_deployments(name=None, namespace=None):
    if name:
        if namespace:
            run_kubectl_command(["delete", "deployments", name, "-n", namespace])
        else:
            run_kubectl_command(["delete", "deployments", name])
    else:
        ai_prompt = "What happens when I run the kubectl delete deployments command without a name?"
        ai_response = generate_ai_response(ai_prompt)
        print(ai_response)

def apply_resource(file=None):
    if file:
        run_kubectl_command(["apply", "-f", file])
    else:
        ai_prompt = "What happens when I run the kubectl apply command without a file?"
        ai_response = generate_ai_response(ai_prompt)
        print(ai_response)

def describe_resource(resource_type, name=None, namespace=None):
    if name:
        if namespace:
            run_kubectl_command(["describe", resource_type, name, "-n", namespace])
        else:
            run_kubectl_command(["describe", resource_type, name])
    else:
        ai_prompt = f"What happens when I run the kubectl describe {resource_type} command without a name?"
        ai_response = generate_ai_response(ai_prompt)
        print(ai_response)

def get_logs(name=None, namespace=None):
    if name:
        if namespace:
            run_kubectl_command(["logs", name, "-n", namespace])
        else:
            run_kubectl_command(["logs", name])
    else:
        ai_prompt = "What happens when I run the kubectl logs command without a name?"
        ai_response = generate_ai_response(ai_prompt)
        print(ai_response)

def edit_resource(resource_type, name=None, namespace=None):
    if name:
        cmd = ["edit", resource_type, name]
        if namespace:
            cmd.extend(["-n", namespace])
        run_kubectl_command(cmd)
    else:
        ai_prompt = f"What happens when I run the kubectl edit {resource_type} command without a name?"
        ai_response = generate_ai_response(ai_prompt)
        print(ai_response)

def exec_command(pod_name, namespace=None, container=None, cmd=None):
    if not cmd:
        print("Error: No command provided", file=sys.stderr)
        sys.exit(1)

    kubectl_cmd = ["exec", pod_name]
    if namespace:
        kubectl_cmd.extend(["-n", namespace])
    if container:
        kubectl_cmd.extend(["-c", container])

    kubectl_cmd.append("--")
    kubectl_cmd.extend(cmd)

    run_kubectl_command(kubectl_cmd)

def expose_resource(resource_type, name, port, target_port=None, service_name=None, namespace=None):
    kubectl_cmd = ["expose", resource_type, name, "--port", str(port)]
    
    if target_port:
        kubectl_cmd.extend(["--target-port", str(target_port)])
    if service_name:
        kubectl_cmd.extend(["--name", service_name])
    if namespace:
        kubectl_cmd.extend(["-n", namespace])

    run_kubectl_command(kubectl_cmd)

def cordon_uncordon_node(node_name, action):
    if action not in ["cordon", "uncordon"]:
        print(f"Error: Invalid action '{action}', only 'cordon' or 'uncordon' are allowed", file=sys.stderr)
        sys.exit(1)

    kubectl_cmd = [action, node_name]
    run_kubectl_command(kubectl_cmd)

def drain_node(node_name, delete_local_data=False, force=False, ignore_daemonsets=False, namespace=None):
    kubectl_cmd = ["drain", node_name]

    if delete_local_data:
        kubectl_cmd.append("--delete-local-data")
    if force:
        kubectl_cmd.append("--force")
    if ignore_daemonsets:
        kubectl_cmd.append("--ignore-daemonsets")
    if namespace:
        kubectl_cmd.extend(["-n", namespace])

    run_kubectl_command(kubectl_cmd)

def label_annotate_resource(resource_type, name, labels_annotations, action):
    if action not in ["label", "annotate"]:
        print(f"Error: Invalid action '{action}', only 'label' or 'annotate' are allowed", file=sys.stderr)
        sys.exit(1)

    kubectl_cmd = [action, resource_type, name]
    for key, value in labels_annotations.items():
        kubectl_cmd.append(f"{key}={value}")

    run_kubectl_command(kubectl_cmd)

def scale_resource(resource_type, name, replicas, namespace=None):
    kubectl_cmd = ["scale", resource_type, name, f"--replicas={replicas}"]
    if namespace:
        kubectl_cmd.extend(["-n", namespace])

    run_kubectl_command(kubectl_cmd)

def taint_node(node, key, effect, value=None):
    kubectl_cmd = ["taint", "nodes", node, f"{key}={value if value else ''}:{effect}"]
    run_kubectl_command(kubectl_cmd)

def cordon_uncordon_drain_node(node, action):
    if action not in ["cordon", "uncordon", "drain"]:
        print(f"Error: Invalid action '{action}', only 'cordon', 'uncordon', or 'drain' are allowed", file=sys.stderr)
        sys.exit(1)

    kubectl_cmd = [action, "nodes", node]
    run_kubectl_command(kubectl_cmd)

# Add more functions for the new commands here

parser = argparse.ArgumentParser(description="brickctl - A CLI tool to provide AI insights into K8s deployments")
subparsers = parser.add_subparsers(dest="command")

get_parser = subparsers.add_parser("get", help="Get resources from the cluster")
get_parser.add_argument("resource", help="Resource type to get (e.g., deployments, pods)")
get_parser.add_argument("-n", "--namespace", help="Namespace of the resource")

create_parser = subparsers.add_parser("create", help="Create a resource from a file")
create_parser.add_argument("file", help="Path to the resource file", nargs="?")

delete_parser = subparsers.add_parser("delete", help="Delete a resource from a file")
delete_parser.add_argument("resource_type", help="Resource type to delete (e.g., deployments, pods)")
delete_parser.add_argument("name", help="Name of the resource to delete")
delete_parser.add_argument("-n", "--namespace", help="Namespace of the resource")

apply_parser = subparsers.add_parser("apply", help="Apply a resource from a file")
apply_parser.add_argument("file", help="Path to the resource file")

describe_parser = subparsers.add_parser("describe", help="Describe a resource")
describe_parser.add_argument("resource_type", help="Resource type to describe (e.g., deployments, pods)")
describe_parser.add_argument("name", help="Name of the resource to describe")
describe_parser.add_argument("-n", "--namespace", help="Namespace of the resource")

logs_parser = subparsers.add_parser("logs", help="Get logs of a container")
logs_parser.add_argument("name", help="Name of the container")
logs_parser.add_argument("-n", "--namespace", help="Namespace of the container")

edit_parser = subparsers.add_parser("edit", help="Edit a resource")
edit_parser.add_argument("resource_type", help="Resource type to edit (e.g., deployments, pods)")
edit_parser.add_argument("name", help="Name of the resource to edit")
edit_parser.add_argument("-n", "--namespace", help="Namespace of the resource")

rollout_parser = subparsers.add_parser("rollout", help="Manage the rollout of a resource")
rollout_parser.add_argument("action", help="Action to perform on the rollout (e.g., status, pause, resume, undo)")
rollout_parser.add_argument("resource_type", help="Resource type to manage (e.g., deployments, statefulsets)")
rollout_parser.add_argument("name", help="Name of the resource")
rollout_parser.add_argument("-n", "--namespace", help="Namespace of the resource")

scale_parser = subparsers.add_parser("scale", help="Scale a resource")
scale_parser.add_argument("resource_type", help="Resource type to scale (e.g., deployments, statefulsets)")
scale_parser.add_argument("name", help="Name of the resource to scale")
scale_parser.add_argument("--replicas", type=int, required=True, help="Number of replicas")
scale_parser.add_argument("-n", "--namespace", help="Namespace of the resource")

taint_parser = subparsers.add_parser("taint", help="Update the taints on one or more nodes")
taint_parser.add_argument("node_name", help="Name of the node to taint")
taint_parser.add_argument("taint", help="Taint to apply in the format key=value:effect")

top_parser = subparsers.add_parser("top", help="Display resource (CPU/Memory/Storage) usage")
top_parser.add_argument("resource_type", help="Resource type to display usage for (e.g., node, pod)")
top_parser.add_argument("name", nargs="?", help="Name of the resource (optional)")
top_parser.add_argument("-n", "--namespace", help="Namespace of the resource")

annotate_parser = subparsers.add_parser("annotate", help="Update the annotations on a resource")
annotate_parser.add_argument("resource_type", help="Resource type to annotate (e.g., deployments, pods)")
annotate_parser.add_argument("name", help="Name of the resource to annotate")
annotate_parser.add_argument("annotation", help="Annotation to apply in the format key=value")
annotate_parser.add_argument("-n", "--namespace", help="Namespace of the resource")

cordon_parser = subparsers.add_parser("cordon", help="Mark node as unschedulable")
cordon_parser.add_argument("node_name", help="Name of the node to cordon")

uncordon_parser = subparsers.add_parser("uncordon", help="Mark node as schedulable")
uncordon_parser.add_argument("node_name", help="Name of the node to uncordon")

drain_parser = subparsers.add_parser("drain", help="Drain node in preparation for maintenance")
drain_parser.add_argument("node_name", help="Name of the node to drain")

label_parser = subparsers.add_parser("label", help="Update the labels on a resource")
label_parser.add_argument("resource_type", help="Resource type to label (e.g., deployments, pods)")
label_parser.add_argument("name", help="Name of the resource to label")
label_parser.add_argument("label", help="Label to apply in the format key=value")
label_parser.add_argument("-n", "--namespace", help="Namespace of the resource")

exec_parser = subparsers.add_parser("exec", help="Execute a command in a container")
exec_parser.add_argument("pod_name", help="Name of the pod containing the container")
exec_parser.add_argument("command", nargs="+", help="Command to execute inside the container")
exec_parser.add_argument("-n", "--namespace", help="Namespace of the pod")
exec_parser.add_argument("-c", "--container", help="Name of the container in which to execute the command")

expose_parser = subparsers.add_parser("expose", help="Expose a resource as a new Kubernetes service")
expose_parser.add_argument("resource_type", help="Resource type to expose (e.g., deployments, pods)")
expose_parser.add_argument("name", help="Name of the resource to expose")
expose_parser.add_argument("--port", type=int, required=True, help="Port that the service should serve on")
expose_parser.add_argument("--target-port", type=int, help="Port on the resource to forward to")
expose_parser.add_argument("--name", help="Name of the new service")
expose_parser.add_argument("-n", "--namespace", help="Namespace of the resource")

services_parser = subparsers.add_parser("services", help="Display services in the cluster")
services_parser.add_argument("-n", "--namespace", help="Namespace of the services")

serviceaccount_parser = subparsers.add_parser("serviceaccount", help="Display service accounts in the cluster")
serviceaccount_parser.add_argument("-n", "--namespace", help="Namespace of the service accounts")

statefulsets_parser = subparsers.add_parser("statefulsets", help="Display stateful sets in the cluster")
statefulsets_parser.add_argument("-n", "--namespace", help="Namespace of the stateful sets")


# Add more parsers for the new commands here

args = parser.parse_args()

if args.command == "get":
    namespace = args.namespace
    resource = args.resource.lower()
    if resource == "deployments":
        get_deployments(namespace)
    elif resource == "pods":
        get_pods(namespace)
    elif resource == "namespaces":
        get_namespaces()
    elif resource == "services":
        get_services(namespace)
    elif resource == "serviceaccounts":
        get_serviceaccounts(namespace)
    elif resource == "statefulsets":
        get_statefulsets(namespace)
    else:
        print(f"Unsupported resource type: {resource}", file=sys.stderr)
        sys.exit(1)
elif args.command == "create":
    create_resource(args.file)
elif args.command == "delete":
    resource_type = args.resource_type.lower() + "s"
    name = args.name
    namespace = args.namespace
    delete_resource(resource_type, name, namespace)
elif args.command == "apply":
    apply_resource(args.file)
elif args.command == "describe":
    resource_type = args.resource_type.lower() + "s"
    name = args.name
    namespace = args.namespace
    describe_resource(resource_type, name, namespace)
elif args.command == "logs":
    name = args.name
    namespace = args.namespace
    get_logs(name, namespace)
elif args.command == "edit":
    resource_type = args.resource_type.lower() + "s"
    name = args.name
    namespace = args.namespace
    edit_resource(resource_type, name, namespace)
# Add more conditions for the new commands here


