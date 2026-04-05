# Bluetooth Tracker for Pico W 🔍

## What Does This Code Do? 

Imagine you have a special robot (called a **Raspberry Pi Pico W**) that's really good at listening for Bluetooth signals — kind of like how a dog can hear things humans can't! 

This code turns your Pico W into a **Bluetooth Detective** that:

1. **Listens for Bluetooth Signals** 📡
   - It continuously scans for nearby Bluetooth devices (like fitness trackers, headphones, or special sensors)
   - When it finds a device with a special code it's looking for, it "catches" it!

2. **Connects to Wi-Fi** 🌐
   - The Pico W connects to your home Wi-Fi network
   - This lets it talk to other computers and services

3. **Sends Messages** 💬
   - When it detects a Bluetooth device, it sends information about it to an MQTT server (a message service)
   - The message includes: which device was found, how strong the signal is, the exact time, and what building/room it's in

4. **Blinks an LED** 💡
   - The built-in LED blinks to show what's happening (like it's thinking or saying "I found something!")

## How It Works (Simple Version) 🏗️

```
START
  ↓
WiFi Connection ✓
  ↓
MQTT Connection ✓
  ↓
Blink! Listen for Bluetooth Signals...
  ↓
Found a Device! → Send Message to MQTT
  ↓
Repeat over and over!
```

## What You Need to Set Up 🛠️

Before the Pico W can work, you need to tell it:
- Your **WiFi name** and **password**
- The **MQTT server address** (where to send messages)
- What **building, floor, and room** it's in
- The **message topic** (like an address for messages)

You can do this in the `config.json` file or through a Bluetooth setup mode.

## The Files Explained 📂

- **`main.py`** - The boss! This starts everything up and keeps the detector running
- **`scanner.py`** - The detective! This looks for Bluetooth signals and catches the special ones
- **`networking.py`** - The communicator! This helps the Pico connect to Wi-Fi
- **`configuration.py`** - The memory! This remembers all your settings
- **`pairing.py`** - The teacher! This helps you set up the Pico the first time
- **`config.json`** - The settings file! You write your Wi-Fi and MQTT info here

## What's Happening in the Scanner 🔍

The scanner:
1. Starts listening for Bluetooth signals
2. Looks at each signal's special code
3. If it matches the code it's hunting for (`DFFB48D2B060D0F5A710`), it wakes up!
4. It collects information: the device's address, signal strength (RSSI), and the time
5. It sends all this data to the MQTT server
6. The LED blinks to celebrate! 🎉
7. Then it goes back to listening again...

## Simple Example 📝

Like a neighborhood watch!
- 👀 Every 2 seconds, the Pico looks around
- 📍 It says "Hey! I found a device at MAC address: `AA:BB:CC:DD:EE:FF`"
- 📊 Signal strength: `-45 dBm` (pretty strong!)
- ⏰ Time: `1234567890`
- 📤 Sends message: `"Building 5, Floor 2, Room 101"`

## Requirements 🔧

- Raspberry Pi Pico W (with Wi-Fi and Bluetooth)
- MicroPython firmware
- Libraries: `aioble`, `umqtt`, `asyncio` (already included!)
- A Wi-Fi network
- An MQTT server (like a message relay station)

---

**In one sentence:** This code turns your Pico W into a smart Bluetooth detector that listens for signals and tells a server what it found! 🎯