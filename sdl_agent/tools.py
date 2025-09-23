# tools.py

from instruments import *
from robotmotion import *
from store import *
from observation import *

def ocp_measurement(i: int) -> Observation:
    obs = start_obs(step="measurement", tool="ocp_measurement", args={"i": i})
    try:
        uFactory_xArm.pick_sample_from_bed(i)
        uFactory_xArm.place_sample_to_measurementstation()
        v = instruments.ocp_measurement_step()
        log_measurement("ocp", i, v, meta={"pose": "measurementstation"})
        uFactory_xArm.pick_sample_from_measurementstation()
        uFactory_xArm.place_sample_to_bed(i)
        obs = finish_ok(obs, value=v, extra_meta={"pose": "measurementstation"})
    except Exception as e:
        obs = finish_err(obs, e)
    finally:
        log_observation(obs)
    return obs

def ca_measurement(i: int) -> Observation:
    obs = start_obs(step="measurement", tool="ca_measurement", args={"i": i})
    try:
        uFactory_xArm.pick_sample_from_bed(i)
        uFactory_xArm.place_sample_to_measurementstation()
        v = instruments.ca_measurement_step()
        log_measurement("ca", i, v, meta={"pose": "measurementstation"})
        uFactory_xArm.pick_sample_from_measurementstation()
        uFactory_xArm.place_sample_to_bed(i)
        obs = finish_ok(obs, value=v, extra_meta={"pose": "measurementstation"})
    except Exception as e:
        obs = finish_err(obs, e)
    finally:
        log_observation(obs)
    return obs

def cv_measurement(i: int) -> Observation:
    obs = start_obs(step="measurement", tool="cv_measurement", args={"i": i})
    try:
        uFactory_xArm.pick_sample_from_bed(i)
        uFactory_xArm.place_sample_to_measurementstation()
        v = instruments.cv_measurement_step()
        log_measurement("cv", i, v, meta={"pose": "measurementstation"})
        uFactory_xArm.pick_sample_from_measurementstation()
        uFactory_xArm.place_sample_to_bed(i)
        obs = finish_ok(obs, value=v, extra_meta={"pose": "measurementstation"})
    except Exception as e:
        obs = finish_err(obs, e)
    finally:
        log_observation(obs)
    return obs

def bring_sample_to_user(i: int) -> Observation:
    obs = start_obs(step="handover", tool="bring_sample_to_user", args={"i": i})
    try:
        uFactory_xArm.pick_sample_from_bed(i)
        uFactory_xArm.place_sample_to_userarea()
        obs = finish_ok(obs, extra_meta={"target": "userarea"})
    except Exception as e:
        obs = finish_err(obs, e)
    finally:
        log_observation(obs)
    return obs

def collect_sample_from_user(i: int) -> Observation:
    obs = start_obs(step="handover", tool="collect_sample_from_user", args={"i": i})
    try:
        uFactory_xArm.pick_sample_from_userarea()
        uFactory_xArm.place_sample_to_bed(i)
        obs = finish_ok(obs, extra_meta={"source": "userarea"})
    except Exception as e:
        obs = finish_err(obs, e)
    finally:
        log_observation(obs)
    return obs

def go_home() -> Observation:
    obs = start_obs(step="navigation", tool="go_home", args={})
    try:
        uFactory_xArm.move_to(uFactory_xArm.home)
        obs = finish_ok(obs, extra_meta={"pose": "home"})
    except Exception as e:
        obs = finish_err(obs, e)
    finally:
        log_observation(obs)
    return obs