import subprocess

def install_package(package, version=None):
    if version:
        package_specifier = f"{package}=={version}"
    else:
        package_specifier = package

    try:
        subprocess.check_call(['pip', 'install', package_specifier])
        print(f"Successfully installed {package_specifier}")
    except subprocess.CalledProcessError:
        print(f"Error installing {package_specifier}")

if __name__ == "__main__":
    install_package('bitarray', '2.9.2')
