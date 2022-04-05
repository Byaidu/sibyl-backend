# sibyl-backend

## Workflow Overview

```mermaid
sequenceDiagram
Frontend->>Keystone:Username + Password
Keystone->>Frontend:Token
Frontend->>Backend:Token + Request
Backend->>Keystone:Verify Token
Keystone->>Backend:Verify Result
Backend->>NTFS:Operate File
NTFS->>Backend:Operate Result
Backend->>Frontend:Request Result
```

## Backend Pipeline Overview

```mermaid
stateDiagram-v2
state Pipeline{
    direction LR
	Backend:Backend
    Backend:Directory
    Backend:File
    Backend:Info
    [*] --> cors
    cors --> authtoken
    authtoken --> Backend
    Backend --> NTFS
}
```

## Keystone RBAC Overview

```mermaid
stateDiagram-v2
Role_admin:Role_admin
Role_admin:Browse
Role_admin:Download
Role_admin:Upload
Role_reader:Role_reader
Role_reader:Browse
Role_reader:Download
state Group_standard {
    state Group_premium {
        state Group_admin {
            admin
        }
        nova
        glance
    }
    demo
    neutron
    cinder
}
state Project_* {
	Project_admin
	Project_nova
	Project_glance
	Project_public
}
Groupstandard:Group_standard
Groupadmin:Group_admin
Grouppremium:Group_premium
Groupadmin --> Project_* : admin
Grouppremium --> Project_public : admin
Groupstandard --> Project_public : reader
admin --> Project_admin : admin
nova --> Project_nova : admin
glance --> Project_glance : admin
```

## Project setup

1. Connect to the database server

```
sudo mysql
```

2. Create the sibyl database

```
CREATE DATABASE sibyl;
USE sibyl;
CREATE TABLE user (name VARCHAR(255), info VARCHAR(255));
```

3. Configure RBAC rules

```
./init_keystone.sh
```

## Project deploy

```
python myService.py
```
