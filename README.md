## Helper Script Usage

Steps:
1. Start the VM
2. Start the respective docker container

VM Name: *llm-inference-vm-1* Contaner Name: *llama-13b* SSH Port: *221* Inference Port: *8081* Username: *llm-inference-vm-1-user* Key Path: *llm-inference-vm-1_key.pem*

VM Name: *llm-inference-vm-2* Contaner Name: *falcon-40b* SSH Port: *222* Inference Port: *8082* Username: *llm-inference-vm-2-user* Key Path: *llm-inference-vm-2_key.pem*

VM Name: *llm-inference-vm-3* Contaner Name: *llama-70b* SSH Port: *223* Inference Port: *8083* Username: *llm-inference-vm-3-user* Key Path: *llm-inference-vm-3_key.pem*

VM Name: *llm-inference-vm-4* Contaner Name: *h2ogpt-4096-llama2-70b-chat* SSH Port: *224* Inference Port: *8084* Username: *llm-inference-vm-4-user* Key Path: *llm-inference-vm-4_key.pem*

Code Example

    parser.add_argument("-n", "--vm_name", required=True)
    parser.add_argument(
        "-a",
        "--action",
        required=True,
        choices=["start-vm", "stop-vm", "start-container"],
    )
    parser.add_argument("-ip", "--public_ip", default=None)
    parser.add_argument("-po", "--port", default=None)
    parser.add_argument("-us", "--username", default=None)
    parser.add_argument("-kp", "--key_path", default=None)
    parser.add_argument("-cn", "--container_name", default=None)

    VM Start Example: python .\helper.py --vm_name llm-inference-vm-1 --action start-vm
    VM Stop Example: python .\helper.py --vm_name llm-inference-vm-1 --action stop-vm

    Container Start Example: python .\helper.py --vm_name llm-inference-vm-1 --action start-container --public_ip 20.23.216.140 --port 221 --username llm-inference-vm-1-user --key_path llm-inference-vm-1_key.pem --container_name llama-13b



## Helper Class Usage

### VM Operations
    from helper import VMManager

    my_vm_manager = VMManager()

    my_vm_manager.stop_vm('llm-inference-vm')

### SSH Operations

First time setup

    ssh = my_vm_manager.establish_ssh_connection_to_vm(public_ip='20.23.216.140', port='221', username='llm-inference-vm-user', key_path='llm-inference-vm_key.pem')

    command = """sudo docker run -d --gpus all --shm-size 1g -p 8080:80 -v $PWD/data:/data ghcr.io/huggingface/text-generation-inference:0.9 --model-id 'tiiuae/falcon-40b-instruct' --num-shard 2 --trust-remote-code --revision 1e7fdcc9f45d13704f3826e99937917e007cd975"""
    my_vm_manager.run_ssh_command_on_vm(ssh=ssh, command=command)

    command = """docker ps"""
    my_vm_manager.run_ssh_command_on_vm(ssh=ssh, command=command)

### Troubleshooting

After stopping the VM and THEN starting it, it should be sufficient to simply run the below docker command to get the endpoint up, which simply starts the already existing container present in the VM.

    contianer names: 
    falcon-40b - Falcon Instruct 40B
    llama-13b - Llama V2 13B
    llama-70b - Llama V2 70B

    command = """docker start <docker-container-name>"""
    my_vm_manager.run_ssh_command_on_vm(ssh=ssh, command=command)

### HF Inference Image Usage

    Usage: text-generation-launcher <--model-id <MODEL_ID>|--revision <REVISION>|--sharded <SHARDED>|--num-shard <NUM_SHARD>|--quantize <QUANTIZE>|--dtype <DTYPE>|--trust-remote-code|--max-concurrent-requests <MAX_CONCURRENT_REQUESTS>|--max-best-of <MAX_BEST_OF>|--max-stop-sequences <MAX_STOP_SEQUENCES>|--max-input-length <MAX_INPUT_LENGTH>|--max-total-tokens <MAX_TOTAL_TOKENS>|--waiting-served-ratio <WAITING_SERVED_RATIO>|--max-batch-prefill-tokens <MAX_BATCH_PREFILL_TOKENS>|--max-batch-total-tokens <MAX_BATCH_TOTAL_TOKENS>|--max-waiting-tokens <MAX_WAITING_TOKENS>|--hostname <HOSTNAME>|--port <PORT>|--shard-uds-path <SHARD_UDS_PATH>|--master-addr <MASTER_ADDR>|--master-port <MASTER_PORT>|--huggingface-hub-cache <HUGGINGFACE_HUB_CACHE>|--weights-cache-override <WEIGHTS_CACHE_OVERRIDE>|--disable-custom-kernels|--json-output|--otlp-endpoint <OTLP_ENDPOINT>|--cors-allow-origin <CORS_ALLOW_ORIGIN>|--watermark-gamma <WATERMARK_GAMMA>|--watermark-delta <WATERMARK_DELTA>|--ngrok|--ngrok-authtoken <NGROK_AUTHTOKEN>|--ngrok-domain <NGROK_DOMAIN>|--ngrok-username <NGROK_USERNAME>|--ngrok-password <NGROK_PASSWORD>|--env>


