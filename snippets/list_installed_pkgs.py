import pkg_resources

def get_installed_packages():
    """Get a list of installed packages and their versions."""
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
       for i in installed_packages])
    return installed_packages_list

def main():
    installed_packages = get_installed_packages()
    for package in installed_packages:
        print(package)

if __name__ == "__main__":
    main()
