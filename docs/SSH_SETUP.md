# SSH Setup for EC2 Access

The `ssh gladly-ec2` command works because of a local SSH configuration file that's not part of the repository. This guide explains how to set it up on a new machine.

## Why `ssh gladly-ec2` Works

The command uses an SSH alias defined in your local `~/.ssh/config` file (or `C:\Users\<username>\.ssh\config` on Windows). This file is **not** tracked in git for security reasons.

## Setup Instructions

### Step 1: Get the EC2 Key File

You need the private key file (`gladly-key.pem` or similar) that was used when creating the EC2 instance.

#### Where to put the key

**Keep the key outside this repo and maintain it separately.**

- **Do not** put it inside the `gladly-conversation-analyzer` project folder. Even though `*.pem` is in `.gitignore`, project folders get copied, shared, and deleted; keys should live in a dedicated place.
- **Recommended (Linux/Mac):** Put it in your SSH directory with your other keys, e.g. `~/.ssh/gladly-key.pem`. That keeps all keys in one place and makes the path in `~/.ssh/config` simple and consistent across machines.
- **Windows:** Use a dedicated folder outside any repo, e.g. `C:\Users\<username>\.ssh\gladly-key.pem` or another path you use only for keys.

The file should:
- **NOT** be committed to git (it's in `.gitignore`)
- Be stored securely on your machine (e.g. `~/.ssh/`)
- Have proper permissions (on Linux/Mac: `chmod 400 gladly-key.pem`)

### Step 2: Find the EC2 Instance IP Address

You can find the current public IP address by:
1. Logging into AWS Console → EC2 → Instances
2. Looking at the instance details
3. **Note**: The IP address may change if you stop/start the instance

Current configuration (as of last update):
- **HostName**: `3.150.69.20` (check AWS Console for current IP)
- **User**: `ec2-user`
- **Key File**: Path to your `.pem` file

### Step 3: Create SSH Config File

#### On Windows (PowerShell):

```powershell
# Create .ssh directory if it doesn't exist
if (-not (Test-Path "$env:USERPROFILE\.ssh")) {
    New-Item -ItemType Directory -Path "$env:USERPROFILE\.ssh"
}

# Add SSH config entry (put gladly-key.pem in .ssh or another folder outside any repo)
@"
Host gladly-ec2
    HostName 3.150.69.20
    User ec2-user
    IdentityFile C:\Users\YOUR_USERNAME\.ssh\gladly-key.pem
    StrictHostKeyChecking no
"@ | Out-File -FilePath "$env:USERPROFILE\.ssh\config" -Append -Encoding utf8
```

**Important**: Replace `YOUR_USERNAME` with your Windows username, or use the path where you stored the key (outside any code repo).

#### On Linux/Mac:

```bash
# Create .ssh directory if it doesn't exist
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add SSH config entry (uses recommended key location ~/.ssh/gladly-key.pem)
cat >> ~/.ssh/config << 'EOF'
Host gladly-ec2
    HostName 3.150.69.20
    User ec2-user
    IdentityFile ~/.ssh/gladly-key.pem
    StrictHostKeyChecking no
EOF

# Set proper permissions
chmod 600 ~/.ssh/config
chmod 400 ~/.ssh/gladly-key.pem
```

**Important**: 
- If you put the key elsewhere, replace `~/.ssh/gladly-key.pem` in the config with that path.
- Make sure the key file has correct permissions: `chmod 400 ~/.ssh/gladly-key.pem` (or your path).

### Step 4: Update IP Address When Needed

If the EC2 instance IP changes (after stop/start), update the `HostName` in your SSH config:

**Windows:**
```powershell
# Edit the config file
notepad "$env:USERPROFILE\.ssh\config"
```

**Linux/Mac:**
```bash
# Edit the config file
nano ~/.ssh/config
# or
vim ~/.ssh/config
```

### Step 5: Test Connection

```bash
ssh gladly-ec2
```

If it works, you should be connected to your EC2 instance!

## Troubleshooting

### "Permission denied (publickey)"
- Verify the key file path in your SSH config is correct
- On Linux/Mac, ensure key file permissions: `chmod 400 gladly-key.pem`
- Verify the key file matches the one registered with AWS

### "Host key verification failed"
- The `StrictHostKeyChecking no` option should prevent this
- If it still occurs, remove the old host key: `ssh-keygen -R 3.150.69.20`

### "Could not resolve hostname"
- Check that the IP address in your config matches the current EC2 instance IP
- Verify you have internet connectivity

### "Connection timed out"
- Check AWS Security Group allows SSH (port 22) from your IP
- Verify the EC2 instance is running
- Check if the IP address has changed

## Security Notes

- **Never commit** your `.pem` key file to git
- **Never commit** your `~/.ssh/config` file if it contains sensitive paths
- Consider using AWS Systems Manager Session Manager for more secure access
- Rotate keys periodically for better security

## Alternative: Use Full SSH Command

If you don't want to set up SSH config, you can always use the full command:

```bash
ssh -i /path/to/gladly-key.pem ec2-user@3.150.69.20
```

Replace the IP address with the current EC2 instance IP from AWS Console.

