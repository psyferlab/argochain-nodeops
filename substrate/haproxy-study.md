I wanted to create an extensively covered HAProxy setup that would only be\
rivaled by proprietary tools such as Amazon's ELB.\
\
Here's an updated `haproxy.cfg` configuration that includes these requirements:

### HAProxy Configuration

1. **Install HAProxy:**
   Ensure you have HAProxy installed on your server.

   ```bash
   # Debian/Ubuntu
   sudo apt update
   sudo apt install haproxy

   # Red Hat/CentOS
   sudo yum install haproxy
   ```

2. **Configure HAProxy:**
   Below is an example `haproxy.cfg` file for your Substrate nodes:

   ```plaintext
   global
       log /dev/log local0
       log /dev/log local1 notice
       chroot /var/lib/haproxy
       stats socket /run/haproxy/admin.sock mode 660 level admin
       stats timeout 30s
       user haproxy
       group haproxy
       daemon

   defaults
       log global
       option tcplog
       option dontlognull
       timeout connect 5000ms
       timeout client  50000ms
       timeout server  50000ms

   frontend substrate_tcp
       bind *:30333
       default_backend substrate_nodes_tcp

   backend substrate_nodes_tcp
       balance roundrobin
       server node1 192.168.1.101:30333 check
       server node2 192.168.1.102:30333 check
       server node3 192.168.1.103:30333 check

   frontend substrate_rpc_http
       bind *:9933
       mode http
       option httplog
       default_backend substrate_nodes_rpc_http

   backend substrate_nodes_rpc_http
       mode http
       balance roundrobin
       option httpchk GET /health
       http-check expect status 200
       server node1 192.168.1.101:9933 check
       server node2 192.168.1.102:9933 check
       server node3 192.168.1.103:9933 check

   frontend substrate_rpc_ws
       bind *:9944
       mode http
       option httplog
       default_backend substrate_nodes_rpc_ws

   backend substrate_nodes_rpc_ws
       mode http
       balance roundrobin
       option httpchk GET /health
       http-check expect status 200
       server node1 192.168.1.101:9944 check
       server node2 192.168.1.102:9944 check
       server node3 192.168.1.103:9944 check

   listen stats
       bind *:8404
       stats enable
       stats uri /stats
       stats auth admin:password
   ```

### Explanation

- **Global and Defaults Sections:** Standard HAProxy settings for logging and timeouts.
- **Frontend and Backend for TCP (30333):**
  - `frontend substrate_tcp` handles incoming TCP traffic on port 30333.
  - `backend substrate_nodes_tcp` balances the traffic between the Substrate nodes.
- **Frontend and Backend for HTTP RPC (9933):**
  - `frontend substrate_rpc_http` handles incoming HTTP traffic on port 9933.
  - `backend substrate_nodes_rpc_http` balances the HTTP RPC requests between the Substrate nodes, with health checks.
- **Frontend and Backend for WebSocket RPC (9944):**
  - `frontend substrate_rpc_ws` handles incoming WebSocket traffic on port 9944.
  - `backend substrate_nodes_rpc_ws` balances the WebSocket RPC requests between the Substrate nodes, with health checks.
- **Stats Section:** Provides a web interface for monitoring HAProxy statistics.

### High Availability with Keepalived

For high availability, you can use `keepalived` to manage HAProxy instances and ensure failover between them. Here is an example `keepalived.conf` configuration:

```plaintext
vrrp_script chk_haproxy {
    script "killall -0 haproxy"
    interval 2
    weight 2
}

vrrp_instance VI_1 {
    interface eth0
    state MASTER
    virtual_router_id 51
    priority 101
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass password
    }
    virtual_ipaddress {
        192.168.1.100
    }
    track_script {
        chk_haproxy
    }
}
```

### Setting up Keepalived

1. **Install Keepalived:**

   ```bash
   # Debian/Ubuntu
   sudo apt install keepalived
   sudo systemctl enable keepalived
   sudo systemctl start keepalived

   # Red Hat/CentOS
   sudo yum install keepalived
   sudo systemctl enable keepalived
   sudo systemctl start keepalived
   ```

2. **Configure Keepalived:**
   Place the `keepalived.conf` configuration file in `/etc/keepalived/keepalived.conf`.

### Conclusion

This HAProxy configuration provides a robust load balancing setup for Substrate nodes \
handling TCP traffic on port 30333 and HTTP/WebSocket RPC traffic on ports 9933 and 9944 \
Combined with Keepalived, it ensures high availability and failover capabilities. This \
setup can rival the functionality of Amazon's ELB for our specific use case. \
