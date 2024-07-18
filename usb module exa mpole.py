
import usb
import usb.core
import usb.util

# Find all devices
devices = usb.core.find(find_all=True)

# List all connected USB devices
for device in devices:
    print(f"Device: {device}")
    print(f"  idVendor: {hex(device.idVendor)}")
    print(f"  idProduct: {hex(device.idProduct)}")

# Find a specific device
# Replace with your device's vendor ID and product ID
vendor_id = 0x1234
product_id = 0x5678
device = usb.core.find(idVendor=vendor_id, idProduct=product_id)

if device is None:
    raise ValueError('Device not found')

# Detach kernel driver if necessary
if device.is_kernel_driver_active(0):
    device.detach_kernel_driver(0)

# Set the active configuration
device.set_configuration()

# Get an endpoint instance
cfg = device.get_active_configuration()
intf = cfg[(0, 0)]

# Assume the first endpoint is the one we need
ep = intf[0]

# Read data from the endpoint
# Adjust the size and timeout as needed
try:
    data = device.read(ep.bEndpointAddress, ep.wMaxPacketSize, timeout=1000)
    print(f"Data read from device: {data}")
except usb.core.USBError as e:
    print(f"USBError: {e}")

# Release the device
usb.util.dispose_resources(device)
