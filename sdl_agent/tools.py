# tools.py

from instruments import *
from robotmotion import *
from store import *
from observation import *

def ocp_measurement(i: int) -> Observation:
    """
    Perform an Open Circuit Potential (OCP) measurement on a specified sample.

    The robotic system automates the process of measuring the OCP of a sample. 
    It picks up the sample from its starting slot, moves it to the measurement 
    station, interacts with the measurement device to analyze the sample, and 
    finally returns the sample to its original slot.

    Args:
        i (int): The index of the sample to measure.

    Returns:
        Observation: An object containing details of the measurement process, 
        including the measured value, duration, and metadata.

    Process:
        1. The robot picks up the sample from its designated slot on the bed.
        2. The sample is placed at the measurement station.
        3. The measurement device performs the OCP analysis and returns the result.
        4. The robot retrieves the sample from the measurement station.
        5. The sample is returned to its original slot on the bed.
        6. The observation is logged, including success or error details.

    Example:
        >>> obs = ocp_measurement(1)
        >>> print(obs.feature)
        OCP
        >>> print(obs.value)
        0.123  # Example measured value
    """
    obs = start_obs(step="measurement", tool="ocp_measurement", args={"i": i})
    try:
        uFactory_xArm.pick_sample_from_bed(i)
        uFactory_xArm.place_sample_to_measurementstation()
        f = "OCP"
        v = instruments.ocp_measurement_step()
        uFactory_xArm.pick_sample_from_measurementstation()
        uFactory_xArm.place_sample_to_bed(i)
        obs = finish_ok(obs, feature=f, sample=i, value=v, extra_meta={"pose": "measurementstation"})
    except Exception as e:
        obs = finish_err(obs, e)
    finally:
        log_observation(obs)
    return obs

def ca_measurement(i: int) -> Observation:
    """
    Perform a Chronoamperometry (CA) measurement on a specified sample.

    The robotic system automates the process of measuring the CA of a sample. 
    It picks up the sample from its starting slot, moves it to the measurement 
    station, interacts with the measurement device to analyze the sample, and 
    finally returns the sample to its original slot.

    Args:
        i (int): The index of the sample to measure.

    Returns:
        Observation: An object containing details of the measurement process, 
        including the measured value, duration, and metadata.

    Process:
        1. The robot picks up the sample from its designated slot on the bed.
        2. The sample is placed at the measurement station.
        3. The measurement device performs the CA analysis and returns the result.
        4. The robot retrieves the sample from the measurement station.
        5. The sample is returned to its original slot on the bed.
        6. The observation is logged, including success or error details.

    Example:
        >>> obs = ca_measurement(2)
        >>> print(obs.feature)
        CA
        >>> print(obs.value)
        0.456  # Example measured value
    """    
    obs = start_obs(step="measurement", tool="ca_measurement", args={"i": i})
    try:
        uFactory_xArm.pick_sample_from_bed(i)
        uFactory_xArm.place_sample_to_measurementstation()
        f="CA"
        v = instruments.ca_measurement_step()
        uFactory_xArm.pick_sample_from_measurementstation()
        uFactory_xArm.place_sample_to_bed(i)
        obs = finish_ok(obs,feature=f, sample=i, value=v, extra_meta={"pose": "measurementstation"})
    except Exception as e:
        obs = finish_err(obs, e)
    finally:
        log_observation(obs)
    return obs

def cv_measurement(i: int) -> Observation:
    """
    Perform a Cyclic Voltammetry (CV) measurement on a specified sample.

    The robotic system automates the process of measuring the CV of a sample. 
    It picks up the sample from its starting slot, moves it to the measurement 
    station, interacts with the measurement device to analyze the sample, and 
    finally returns the sample to its original slot.

    Args:
        i (int): The index of the sample to measure.

    Returns:
        Observation: An object containing details of the measurement process, 
        including the measured value, duration, and metadata.

    Process:
        1. The robot picks up the sample from its designated slot on the bed.
        2. The sample is placed at the measurement station.
        3. The measurement device performs the CV analysis and returns the result.
        4. The robot retrieves the sample from the measurement station.
        5. The sample is returned to its original slot on the bed.
        6. The observation is logged, including success or error details.

    Example:
        >>> obs = cv_measurement(3)
        >>> print(obs.feature)
        CV
        >>> print(obs.value)
        0.789  # Example measured value
    """
    obs = start_obs(step="measurement", tool="cv_measurement", args={"i": i})
    try:
        uFactory_xArm.pick_sample_from_bed(i)
        uFactory_xArm.place_sample_to_measurementstation()
        f="CV"
        v = instruments.cv_measurement_step()
        uFactory_xArm.pick_sample_from_measurementstation()
        uFactory_xArm.place_sample_to_bed(i)
        obs = finish_ok(obs, feature=f, sample=i, value=v, extra_meta={"pose": "measurementstation"})
    except Exception as e:
        obs = finish_err(obs, e)
    finally:
        log_observation(obs)
    return obs

def bring_sample_to_user(i: int) -> Observation:
    """
    Bring a specified sample to the user area.

    The robotic system picks up the sample from its designated slot on the bed 
    and places it in the user area for interaction.

    Args:
        i (int): The index of the sample to bring to the user.

    Returns:
        Observation: An object containing details of the operation, including 
        the sample index, duration, and metadata.

    Process:
        1. The robot picks up the sample from its designated slot on the bed.
        2. The sample is placed in the user area.
        3. The observation is logged, including success or error details.

    Example:
        >>> obs = bring_sample_to_user(4)
        >>> print(obs.meta["target"])
        userarea
    """
    obs = start_obs(step="interraction", tool="bring_sample_to_user", args={"i": i})
    try:
        uFactory_xArm.pick_sample_from_bed(i)
        uFactory_xArm.place_sample_to_userarea()
        obs = finish_ok(obs, sample=i, extra_meta={"target": "userarea"})
    except Exception as e:
        obs = finish_err(obs, e)
    finally:
        log_observation(obs)
    return obs

def collect_sample_from_user(i: int) -> Observation:
    """
    Collect a specified sample from the user area and return it to its original slot.

    The robotic system picks up the sample from the user area and places it back 
    in its designated slot on the bed.

    Args:
        i (int): The index of the sample to collect from the user.

    Returns:
        Observation: An object containing details of the operation, including 
        the sample index, duration, and metadata.

    Process:
        1. The robot picks up the sample from the user area.
        2. The sample is returned to its designated slot on the bed.
        3. The observation is logged, including success or error details.

    Example:
        >>> obs = collect_sample_from_user(5)
        >>> print(obs.meta["source"])
        userarea
    """
    obs = start_obs(step="interraction", tool="collect_sample_from_user", args={"i": i})
    try:
        uFactory_xArm.pick_sample_from_userarea()
        uFactory_xArm.place_sample_to_bed(i)
        obs = finish_ok(obs, sample=i, extra_meta={"source": "userarea"})
    except Exception as e:
        obs = finish_err(obs, e)
    finally:
        log_observation(obs)
    return obs

def go_home() -> Observation:
    """
    Move the robotic arm to its home position.

    The robotic system moves to its predefined home position, ensuring it is 
    in a safe and idle state.

    Returns:
        Observation: An object containing details of the operation, including 
        the duration and metadata.

    Process:
        1. The robot moves to its home position.
        2. The observation is logged, including success or error details.

    Example:
        >>> obs = go_home()
        >>> print(obs.meta["pose"])
        home
    """
    obs = start_obs(step="home", tool="go_home", args={})
    try:
        uFactory_xArm.move_to(uFactory_xArm.home)
        obs = finish_ok(obs, extra_meta={"pose": "home"})
    except Exception as e:
        obs = finish_err(obs, e)
    finally:
        log_observation(obs)
    return obs