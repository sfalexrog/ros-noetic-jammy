# Infrastructure and patches for building ROS Noetic for Ubuntu Jammy

## Performing a local, from-source build

1. Install required packages from default Ubuntu repositories:

    ```bash
    sudo apt-get install -y ca-certificates curl python3 python-is-python3 python3-pip build-essential git
    ```

2. Install ROS tools using pip:

    ```bash
    sudo pip3 install --upgrade setuptools rosdep rosinstall_generator vcstool
    ```

3. Initialize rosdep and use our overrides:

    ```bash
    sudo rosdep init
    cp -r rosdep /etc/ros/
    rosdep update
    ```

    The overrides change some Python dependencies to use pip instead of apt versions.

4. Create a base workspace and import sources:

    ```bash
    mkdir ~/ros_ws
    cd ~/ros_ws
    rosinstall_generator desktop_full --rosdistro noetic --deps > noetic-desktop-full.rosinstall
    mkdir ./src
    vcs import --input noetic-desktop.rosinstall ./src
    ```

5. Patch sources wuth the [apply_patches](patches/apply_patches.py) script:

    ```bash
    # IMPORTANT: the script must be run in the workspace directory!
    cd ~/ros_ws
    /path/to/this/repo/patches/apply_patches.py
    ```

6. Install dependencies:

    ```bash
    cd ~/ros_ws
    rosdep install --from-paths ./src --ignore-packages-from-source --rosdistro noetic -y
    ```

7. Build your workspace (this may take a while):

    ```bash
    cd ~/ros_ws
    ./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=RelWithDebInfo
    ```
