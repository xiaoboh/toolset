#!/usr/bin/python
# coding=utf-8
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#


import csv


class TagItem:
    """
    a tag item
    """

    #Number of arguments for a function tag.
    field_arity = 0

    #Name of the class for which this tag is a member or method.
    field_class = ''

    #Name of the enumeration in which this tag is an enumerator.
    field_enum = ''

    #Function in which this tag is defined.  Useful for local
	#variables (and functions).  When functions nest (e.g., in
	#Pascal), the function names are concatenated, separated with
	#'/', so it looks like a path.
    field_function = ''

    # Kind of tag.  The value depends on the language. 
    field_kind = ''

    #Name of the struct in which this tag is a member.
    field_struct = ''

    #Name of the union in which this tag is a member.
    field_union = ''

    #Static (local) tag, with a scope of the specified file.  
    #When the value is empty, {tagfile} is used.
    field_file = ''

    #tag name
    field_name = ''

    #content
    field_content = ''

    #language
    field_language = ''

    def __init__(self, item):
        pass


class ParserCtagsFile:
    """
    use cvs parser ctags's tags file
    """

    fname = ""
    tags = []

    def __init__(self, fname = "./tags"):
        self.fname = fname;
        csvf = csv.reader( open(self.fname), delimiter='\t') 
        
        # load the tags file date to mem 
        for item in csvf:
            # get ctags file opt
            if item[0][0:6] == '!_TAG_':
                if item[0] == '!_TAG_FILE_FORMAT':
                    self.file_format = item[1]
                elif item[0] == '!_TAG_FILE_SORTED':
                    self.file_sorted = item[1]
                elif item[0] == '!_TAG_PROGRAM_AUTHOR':
                    self.prog_author = item[1]
                elif item[0] == '!_TAG_PROGRAM_NAME':
                    self.prog_name = item[1]
                elif item[0] == '!_TAG_PROGRAM_URL':
                    self.prog_url = item[1]
                elif item[0] == '!_TAG_PROGRAM_VERSION':
                    self.prog_ver = item[1]
                continue

            # get all tags item
            self.tags.append( TagItem(item) )


    def get_all(self):
        """
            return all tags 
        """
        return self.tags


    def find_all(self, cmp_func):
        """
        find tag item in all tags
        """
        pass

    def __iter__(self):
        return self.tags

    def next(self):
        pass

