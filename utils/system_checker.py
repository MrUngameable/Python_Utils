import platform
import sys
import psutil
import subprocess


# -----------------------------
# OS / SOFTWARE INFO
# -----------------------------
class OSInfo:
    def __init__(self):
        pass

    def get_os_info(self):
        """
        Returns a dictionary with normailized
        OS Information & OS-specific details
        """

        system = platform.system().lower()

        os_info = {
            "os": None,                         # Windows / Linux / macOS / Unknown
            "os_name": platform.system(),
            "os_version": platform.version(),
            "release": platform.release(),
            "architecture": platform.machine(),
            "python_version": sys.version,
            "details": {}                       # OS-specific info
        }

        if system == "windows":
            os_info["os"] = "windows"
            os_info["details"] = self._get_windows_info()

        elif system == "darwin":
            os_info["os"] = "macos"
            os_info["details"] = self._get_macos_info()

        elif system == "linux":
            os_info["os"] = "linux"
            os_info["details"] = self._get_linux_info()

        else:
            os_info["os"] = "unknown"
        
        return os_info
    
    def get_os(self):
        """
        Returns only the normaized OS name
        """
        return self.get_os_info()["os"]
    
    # ---------------- Windows ----------------
    def _get_windows_info(self):
        info = {}

        try:
            release, version, csd, ptype = platform.win32_ver()

            info["release"] = release           # '7', '10', '11'
            info["version"] = version           # build string
            info["csd"] = csd                   # service pack
            info["platform_type"] = ptype
        
        except Exception as e:
            info["error"] = str(e)
        
        return info
    
    # ---------------- Linux ----------------
    def _get_linux_info(self):
        info = {}

        # Newer Python versions (3.10+) provide this
        try:
            distro = platform.freedesktop_os_release()
            info["distro_name"] = distro.get("NAME")
            info["distro_id"] = distro.get("ID")
            info["version"] = distro.get("VERSION")
            info["version_id"] = distro.get("VERSION_ID")
            info["pretty_name"] = distro.get("PRETTY_NAME")
        
        except Exception:
            # Fallback (minimal but always available)
            info["distro"] = "Unknown"
            info["kernel"] = platform.release()
        
        return info
    
    # ---------------- macOS ----------------
    def _get_macos_info(self):
        info = {}

        try:
            release, versioninfo, machine = platform.mac_ver()

            info["release"] = release               # macOS version number
            info["version_info"] = versioninfo      # ('', '', '')
            info["machine"] = machine               # x86_64 / arm64

            # Human-readable macOS name mapping (optional, partial)
            info["name"] = self._macos_name_from_version(release)
        
        except Exception as e:
            info["error"] = str(e)
        
        return info

    def _macos_name_from_version(self, version):
        """
        Maps macOS version to marketing name (best-effort)
        """
        mapping = {
            "10.15": "Catalina",
            "11": "Big Sur",
            "12": "Monterey",
            "13": "Ventura",
            "14": "Sonoma",
        }

        for key in mapping:
            if version.startswith(key):
                return mapping(key)
        
        return "Unknown"
# -----------------------------


# -----------------------------
# HARDWARE INFO
# -----------------------------
class HardwareInfo:
    def __init__(self):
        pass

    def get_size(self, bytes, suffix="B"):
        """Scale bytes to KB, MB, GB, etc."""
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def get_cpu_info(self):
        info = {}

        info['Physical Cores'] = psutil.cpu_count(logical=False)
        info['Total Cores'] = psutil.cpu_count(logical=True)

        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            info['Max Frequency'] = f"{cpu_freq.max:.2f} MHz"
            info['Min Frequency'] = f"{cpu_freq.min:.2f} MHz"
            info['Current Frequency'] = f"{cpu_freq.current:.2f} MHz"
        
        info['Processor'] = platform.processor()
        return info
    
    def get_memory_info(self):
        svmem = psutil.virtual_memory()

        return {
            "Total": self.get_size(svmem.total),
            "Available Memory": self.get_size(svmem.available),
            "Used Memory": self.get_size(svmem.used),
            "Usage": f"{svmem.percent}%"
        }
    
    def get_disk_info(self):
        partitions = psutil.disk_partitions()
        disk_info = []

        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue

            disk_info.append({
                "Device": partition.device,
                "Mountpoint": partition.mountpoint,
                "File System": partition.fstype,
                "Total Size": self.get_size(usage.total),
                "Used": self.get_size(usage.used),
                "Free": self.get_size(usage.free),
                "Usage": f"{usage.percent}"
            })
        return disk_info
    
    def get_gpu_info(self):
        """
        Returns NVIDIA GPU Info if available, otherwise a message.
        """        
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name,memory.total,driver_version', '--format=csv,noheader'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:
                gpus = []
                for line in result.stdout.strip().split('\n'):
                    name, mem, driver = [x.strip() for x in line.split(',')]
                    gpus.append({
                        "Name": name,
                        "Memory": mem,
                        "Driver": driver
                    })
                return gpus
            else:
                return "No NVIDIA GPU detected."
            
        except FileNotFoundError:
            return "No NVIDIA GPU or 'nvidia-smi' not found."
    
    def get_hardware_info(self):
        """
        Returns all hardware info combined
        """
        return {
            "CPU": self.get_cpu_info(),
            "Memory": self.get_memory_info(),
            "Disks": self.get_disk_info(),
            "GPU": self.get_gpu_info(),
        }
# -----------------------------


# -----------------------------
# COMBINED SYSTEM WRAPPER
# -----------------------------
class Systeminfo:
    def __init__(self):
        self.os_info = OSInfo()
        self.hardware_info = HardwareInfo()
    
    def get_full_system_info(self):
        return {
            "OS": self.os_info.get_os_info(),
            "Hardware": self.hardware_info.get_hardware_info()
        }
# -----------------------------