# dolphin-interview

### Problem 2

Although Puppet and Ansible try to accomplish the same task, there are
a few differences that could affect which is more appropriate to a
given situation.

* Puppet requires an agent process to be running on all managed
  systems to poll a "puppet master" node for configuration changes.
  Ansible uses SSH to execute shell commands on the managed nodes from
  any machine with SSH access to the managed nodes and the desired
  playbooks.

* The polling behaviour of Puppet might be appropriate in a system
  where the configuration can change outside the control of the system
  administrator since it's likely that the Ansible playbooks would
  normally only be run when a configuration change is made or a new
  node is brought online.

* Puppet abstracts away the package manager, meaning that deploying on
  Ubuntu, Redhat, and SuSE might be possible with a single module,
  whereas Ansible would require three separate modules to call out to
  apt, yum, and zypper.

* Puppet has an enterprise edition that comes with some snazzy
  features for managing and provisioning storage, collecting system
  metrics, monitoring events, and RBAC. This could be a benefit over
  Ansible on larger projects.

### Problem 3

Puppet would be more suitable than containers or VMs for configuring
hosts for IO load testing like we do with VPlex. Because what you
really want for testing is access to the HBA, which is attached to a
fixed SAN zone, the overhead of virtualizing the environment presents
no benefits.

### Problem 4

Imagine a setting with lots of homogeneous powerful hardware and a
large varied workload of small services. For example, a cloud service
provider. Containers allow instances of services to be spread out
across the available hardware. A central Docker repository provides a
simple "push" mechanism for configuration changes. As a side note,
Puppet might still be appropriate for the underlying configuration of
the host systems.