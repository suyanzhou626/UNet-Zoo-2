import os
from importlib.machinery import SourceFileLoader
import argparse

import utils

# if not sys_config.running_on_gpu_host:
#     import matplotlib.pyplot as plt

from train_model import UNetModel
import shutil
from data.lidc_data import lidc_data
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

structures_dict = {1: 'RV', 2: 'Myo', 3: 'LV'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script for training")
    parser.add_argument("EXP_PATH", type=str, help="Path to experiment config file")
    parser.add_argument("LOCAL", type=str, help="Is this script run on the local machine or the BIWI cluster?")
    parser.add_argument("dummy", type=str, help="Is the module run with dummy training?")
    args = parser.parse_args()

    config_file = args.EXP_PATH
    config_module = config_file.split('/')[-1].rstrip('.py')

    if args.LOCAL == 'local':
        print('Running with local configuration')
        import config.local_config as sys_config
        import matplotlib.pyplot as plt
    else:
        import config.system as sys_config

    logging.info('Running experiment with script: {}'.format(config_file))

    exp_config = SourceFileLoader(config_module, config_file).load_module()

    log_dir = os.path.join(sys_config.log_root, exp_config.log_dir_name, exp_config.experiment_name)

    utils.makefolder(log_dir)

    shutil.copy(exp_config.__file__, log_dir)
    logging.info('!!!! Copied exp_config file to experiment folder !!!!')

    logging.info('**************************************************************')
    logging.info(' *** Running Experiment: %s', exp_config.experiment_name)
    logging.info('**************************************************************')

    model = UNetModel(exp_config)
    transform = None

    data = lidc_data(sys_config=sys_config, exp_config=exp_config)
    model.test(data, sys_config=sys_config)

    #model.save_model()
