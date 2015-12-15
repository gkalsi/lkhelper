"""
   Copyright 2015 - Gurjant Kalsi <me@gurjantkalsi.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import os

from fabric.api import local, lcd, task

# NOTE: Fill these in.
LK_PROJECT_BASE = os.path.expanduser("~/code/lk")
SOD_PROJECT_BASE = os.path.expanduser("~/code/sod")
OPEN_OCD_BASE = os.path.expanduser("~/code/openocd")

DARTUINO_BUILD_TARGET = "dartuinoP0-test"
DARTUINO_SOD_BUILD_TARGET = "dartuino-p0-fletch"
DISCO_BUILD_TARGET = "stm32f746g-disco-test"
EVAL_BUILD_TARGET = "stm32746g-eval2-test"

class LKTarget:
	def __init__(self, repo_root, target_project, board_cfg, stlink_cfg, bin_dir):
		build_subdir = "build-" + target_project
		full_binary_path = os.path.join(repo_root, bin_dir, build_subdir, "lk.bin")

		program_command_list = ["program", full_binary_path, "reset", "exit", "0x08000000"]
		program_command = " ".join(program_command_list)
		program_command = "\"" + program_command + "\""

		flash_command_list = [
			"openocd",
			"-f", stlink_cfg,
			"-f", board_cfg,
			"-c", program_command
		]

		self.flash_command = " ".join(flash_command_list)
		self.target_project = target_project
		self.repo_root = repo_root


DiscoLKTarget = LKTarget(LK_PROJECT_BASE, DISCO_BUILD_TARGET, "tcl/board/stm32746g_eval.cfg", "tcl/interface/stlink-v2-1.cfg", "")
DartuinioTarget = LKTarget(LK_PROJECT_BASE, DARTUINO_BUILD_TARGET, "tcl/board/stm32746g_eval.cfg", "tcl/interface/stlink-v2.cfg", "")
EvalLKTarget = LKTarget(LK_PROJECT_BASE, EVAL_BUILD_TARGET, "tcl/board/stm32746g_eval.cfg", "tcl/interface/stlink-v2-1.cfg", "")
DiscoSODTarget = LKTarget(SOD_PROJECT_BASE, DISCO_BUILD_TARGET, "tcl/board/stm32746g_eval.cfg", "tcl/interface/stlink-v2-1.cfg", "out")
DartuinoSODTarget = LKTarget(SOD_PROJECT_BASE, DARTUINO_SOD_BUILD_TARGET, "tcl/board/stm32746g_eval.cfg", "tcl/interface/stlink-v2.cfg", "out")

@task
def disco_do():
	build(DiscoLKTarget)
	flash(DiscoLKTarget)

@task
def dartuino_do():
	build(DartuinioTarget)
	flash(DartuinioTarget)

@task
def eval_do():
	build(EvalLKTarget)
	flash(EvalLKTarget)

@task
def sod_do():
	build(DiscoSODTarget)
	flash(DiscoSODTarget)

@task
def sod_dartuino_do():
	build(DartuinoSODTarget)
	flash(DartuinoSODTarget)

def flash(target):
	with lcd(OPEN_OCD_BASE):
		local(target.flash_command)

def build(target):
	make_cmd = "make PROJECT=%s" % target.target_project

	with lcd(target.repo_root):
		local(make_cmd)


