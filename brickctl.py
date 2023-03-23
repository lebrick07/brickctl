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



