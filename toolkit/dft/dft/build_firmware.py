#
# The contents of this file are subject to the Apache 2.0 license you may not
# use this file except in compliance with the License.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
#
# Copyright 2016 DFT project (http://www.debianfirmwaretoolkit.org).
# All rights reserved. Use is subject to license terms.
#
# Debian Firmware Toolkit is the new name of Linux Firmware From Scratch
# Copyright 2014 LFFS project (http://www.linuxfirmwarefromscratch.org).
#
#
# Contributors list :
#
#    William Bonnet     wllmbnnt@gmail.com, wbonnet@theitmakers.com
#
#

""" This module contains the functionnalities needed to create a squashfs compressed file
from a baseos. The squashfs file contains hte operating system, or configuration files, or
anything you decide. They can be stacked in memory to create the read only operating system.
"""

import logging
import os
from cli_command import CliCommand

#
#    Class BuildFirmware
#
class BuildFirmware(CliCommand):
  """This class implements method needed to create the squashfs file(s) used
  to storefirmware content
  """

  # -------------------------------------------------------------------------
  #
  # __init__
  #
  # -------------------------------------------------------------------------
  def __init__(self, dft, project):
    """Default constructor
    """

    # Initialize ancestor
    CliCommand.__init__(self, dft, project)

  # -------------------------------------------------------------------------
  #
  # build_firmware
  #
  # -------------------------------------------------------------------------
  def build_firmware(self):
    """This method implement the business logic of firmware generation.
    Firmware is  squashfs file containing the rootfs generated previously.

    Current version produce only one squashfs file. Algorith is basic...
      . Create target directory if missing
      . Remove existing file
      . Generate the mksquashfs command and add options
      . That's all

    """

    # Ensure firmware generation path exists and is a dir
    if not os.path.isdir(self.project.rootfs_mountpoint):
      logging.critical("The rootfs directory does not exist (" +
                       self.project.rootfs_mountpoint + ")")
      exit(1)

    # Ensure firmware generation path exists and is a dir
    if not os.path.isdir(self.project.firmware_directory):
      os.makedirs(self.project.firmware_directory)

    # Remove existing firmware if needed
    if os.path.isfile(self.project.firmware_filename):
      os.remove(self.project.firmware_filename)

    # Create a new squashfs file from the baseos path
    sudo_command = 'mksquashfs "' +  self.project.rootfs_mountpoint + '" "'
    sudo_command += self.project.firmware_filename + '"'

    # Append arguments if defined in the configuration file
    if "block-size" in self.project.firmware_definition["configuration"]:
      sudo_command += ' -b ' + self.project.firmware_definition["configuration"]["block_size"]

    if "compressor" in self.project.firmware_definition["configuration"]:
      sudo_command += ' -comp ' + self.project.firmware_definition["configuration"]["compressor"]

    if "no-exports" in self.project.firmware_definition["configuration"]:
      if self.project.firmware_definition["configuration"]["no-exports"]:
        sudo_command += ' -no-exports '

    if "no-spare" in self.project.firmware_definition["configuration"]:
      sudo_command += ' -no-spare '

    if "xattrs" in self.project.firmware_definition["configuration"]:
      if self.project.firmware_definition["configuration"]["xattrs"]:
        sudo_command += ' -xattrs '
      if not self.project.firmware_definition["configuration"]["xattrs"]:
        sudo_command += ' -no-xattrs '

    if "no-inode-compression" in self.project.firmware_definition["configuration"]:
      sudo_command += ' -noI '

    if "no-datablock-compression" in self.project.firmware_definition["configuration"]:
      sudo_command += ' -noD '

    if "no-fragmentblock-compression" in self.project.firmware_definition["configuration"]:
      sudo_command += ' -noF '

    if "no-xattrs-compression" in self.project.firmware_definition["configuration"]:
      sudo_command += ' -noX '

    if "use-fragments" in self.project.firmware_definition["configuration"]:
      if self.project.firmware_definition["configuration"]["use-fragments"]:
        sudo_command += ' -always-use-fragments '
      if not self.project.firmware_definition["configuration"]["use-fragments"]:
        sudo_command += ' -no-fragments '

    if "no-duplicate-check" in self.project.firmware_definition["configuration"]:
      if self.project.firmware_definition["configuration"]["no-duplicate-check"]:
        sudo_command += ' -no-duplicates '

    if "all-root" in self.project.firmware_definition["configuration"]:
      if self.project.firmware_definition["configuration"]["all-root"]:
        sudo_command += ' -all-root '

    if "force-uid" in self.project.firmware_definition["configuration"]:
      sudo_command += ' -force-uid '
      sudo_command += self.project.firmware_definition["configuration"]["force-uid"]

    if "force-gid" in self.project.firmware_definition["configuration"]:
      sudo_command += ' -force-gid '
      sudo_command += self.project.firmware_definition["configuration"]["force-gid"]

    if "nopad" in self.project.firmware_definition["configuration"]:
      if self.project.firmware_definition["configuration"]["nopad"]:
        sudo_command += ' -nopad '

    self.execute_command(sudo_command)

# TODO : add control hash and signature according to configuration file options

# TODO
# What is needed in the configuration file
# production:
# #   format: squashfs
# #   option...
# #   alternative to squashfs ? exploded maybe tarball with compression option
# #   target path ?

#        -keep-as-directory
#            if  one source directory is specified, create a root directory contain‐
#            ing that directory, rather than the contents of the directory.

#    Filesystem filter options
#        -p PSEUDO_DEFINITION
#            Add pseudo file definition.

#        -pf PSEUDO_FILE
#            Add list of pseudo file definitions.

#        -sort SORT_FILE
#            sort files according to priorities in SORT_FILE. One file or  dir  with
#            priority per line. Priority -32768 to 32767, default priority 0.

#        -ef EXCLUDE_FILE
#            list of exclude dirs/files. One per line.

#        -wildcards
#            Allow  extended  shell  wildcards  (globbing)  to  be  used  in exclude
#            dirs/files

#        -regex
#            Allow POSIX regular expressions to be used in exclude dirs/files.

#    Filesystem append options
#        -noappend
#            do not append to existing filesystem.

#        -root-becomes NAME
#            when appending source files/directories, make the original root  become
#            a  subdirectory in the new root called NAME, rather than adding the new
#            source items to the original root.



# Later add the possibility to generate several squashfs out of a baseos, and do delta, time based ?
