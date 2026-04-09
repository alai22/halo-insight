#!/bin/bash
# SSH Setup Script for Mac Laptop
# Run this on the Mac where ssh gladly-ec2 doesn't work yet

echo "🔧 Setting up SSH config for gladly-ec2..."

# Step 1: Check if key file exists
echo ""
read -p "Enter the full path to your gladly-key.pem file (e.g., ~/Code/halo-insight/gladly-key.pem): " keyFile

# Expand ~ to home directory
keyFile="${keyFile/#\~/$HOME}"

if [ ! -f "$keyFile" ]; then
    echo "❌ ERROR: Key file not found at: $keyFile"
    echo "Please copy the key file from your Windows laptop first!"
    echo "The key file should be at: C:\\Users\\alai2\\Code\\halo-insight\\gladly-key.pem"
    exit 1
fi

# Set proper permissions on key file
chmod 400 "$keyFile"
echo "✅ Set key file permissions (400)"

# Step 2: Get current EC2 IP (may have changed)
echo ""
read -p "Enter the EC2 instance IP address (current: 3.150.69.20, check AWS Console if unsure): " ec2Ip

# Step 3: Create .ssh directory if it doesn't exist
if [ ! -d "$HOME/.ssh" ]; then
    mkdir -p "$HOME/.ssh"
    chmod 700 "$HOME/.ssh"
    echo "✅ Created .ssh directory"
fi

# Step 4: Check if config already exists and has gladly-ec2 entry
configPath="$HOME/.ssh/config"

if [ -f "$configPath" ]; then
    if grep -q "^Host gladly-ec2" "$configPath"; then
        echo "⚠️  WARNING: 'gladly-ec2' entry already exists in SSH config!"
        read -p "Do you want to overwrite it? (y/n): " overwrite
        if [ "$overwrite" != "y" ]; then
            echo "Aborted. Please manually edit: $configPath"
            exit 0
        fi
        # Remove existing entry
        awk '/^Host gladly-ec2/,/^Host |^$/{if (!/^Host gladly-ec2/ && !/^Host /) next}1' "$configPath" > "$configPath.tmp" && mv "$configPath.tmp" "$configPath"
    fi
fi

# Step 5: Add SSH config entry
cat >> "$configPath" << EOF

Host gladly-ec2
    HostName $ec2Ip
    User ec2-user
    IdentityFile $keyFile
    StrictHostKeyChecking no
EOF

chmod 600 "$configPath"
echo "✅ Added SSH config entry"

# Step 6: Test connection
echo ""
echo "🧪 Testing SSH connection..."
ssh gladly-ec2 "echo 'SSH connection successful!' && hostname"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Setup complete! You can now use: ssh gladly-ec2"
else
    echo ""
    echo "⚠️  Connection test failed. Please check:"
    echo "  1. Key file path is correct: $keyFile"
    echo "  2. EC2 IP address is correct: $ec2Ip"
    echo "  3. EC2 instance is running"
    echo "  4. Security group allows SSH from your IP"
fi

