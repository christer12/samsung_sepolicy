#!/usr/bin/env python
import os
import re
import subprocess
import sys

class Utils():
    @staticmethod
    def flatten(x):

        if isinstance(x, basestring):
            return [x]
    
        result = []
        for el in x:
            #if isinstance(el, (list, tuple)):
            if hasattr(el, "__iter__") and not isinstance(el, basestring):
                result.extend(Utils.flatten(el))
            else:
                result.append(el)
        return result
    
    @staticmethod
    def anchorfy(x):
        new_str = ""
        new_str += "".join([ "^" + chunk + "$ " for chunk in x.split()]) 
        return new_str
    
class SEBuilder(object):
    '''
    Base class for all SE Linux/Android policy builders. The class verifies and generates a list
    of all the policy files to be used for compilation.
    '''
    def __init__(self, root, pol_dirs, base_policy, pol_union, pol_replace, mls_cats, mls_sens, policy_vers):
        self.root = root
        # Add base policy to the search path, but keep track of it since it is special.
        # Ie base policy files typically go first in builders.
        self.pol_dirs = set(Utils.flatten([pol_dirs, base_policy]))
        self.pol_union = set(Utils.flatten(pol_union))
        self.pol_replace = set(Utils.flatten(pol_replace))
        self.mls_cats = mls_cats
        self.mls_sens = mls_sens
        self.policy_vers = policy_vers
        self.policy_files = dict()
        self.base_policy = base_policy
        self._verify()
        self._generate()

    def _verify(self):
        '''
        Verify the configuration
        '''
        print("Verifying configuration")
        # Mls and PolicyVers should be representable as int's
        # Leave them as strings for easy manipulation though
        try:
            self.mls_cats = str(int(self.mls_cats))
            self.mls_sens = str(int(self.mls_sens))
            self.policy_vers = str(int(self.policy_vers))
        except ValueError as e:
            sys.exit(e)
        
        if not os.path.isdir(self.root):
            sys.exit("Root path set to " + self.root + " is not a directory or does not exist!") 

        if not os.path.isdir(os.path.join(self.root, self.base_policy)):
            sys.exit("Base policy set to " + self.base_policy + " is not a directory or does not exist!") 
        
        # The cardinality of the intersection of policy files union and replace must be 0. Else it
        # is an ambiguous request.
        common_intersection = self.pol_replace.intersection(self.pol_union)
        if len(common_intersection) > 0:
            sys.exit("Policy files specified in both BOARD_SEPOLICY_REPLACE and BOARD_SEPOLICY UNTION\n"+ common_intersection)
            
        # Any file specified in replace MUST be found in the BOARD_SEPOLICY_DIRS search path
        for f in self.pol_replace: 
            # Replace files can only exist ONCE on the search path
            replace_file_occurrences = 0
            for d in self.pol_dirs:
                ff = os.path.join(self.root, d, f)
                if os.path.isfile(ff):
                    replace_file_occurrences = replace_file_occurrences + 1
            #Enforce that replace file should have 2 occurrences on the search path, base and user locations
            if replace_file_occurrences != 2:
                sys.exit("File " + f + " specified in BOARD_SEPOLICY_REPLACE but "+ str(replace_file_occurrences) +
                         " of the file were found!")
                
        print("Configuration verified")
                    
    def _generate(self):
        '''
        Generate the hash table of basename to full path list mapping of policy files by adding everything
        in the base policy, plus what was specified in BOARD_SEPOLICY_UNION/REPLACE by searching BOARD_SEPOLICY_DIRS
        '''
        print("Generating file mapping")
        pol_dirs_sans_base = self.pol_dirs.difference(set([self.base_policy]))
        
        #Generate a hastable mapping for all policy files found in policy dirs
        for d in self.pol_dirs:
            for f in os.listdir(os.path.join(self.root, d)):
                # The file name is the "key" in the table
                if f not in self.policy_files:
                    self.policy_files[f] = list()
                
                full_path = os.path.join(os.path.join(self.root, d, f))

                # We create a map from basename to list of found occurrences in the
                # search path. We only add basenames found in UNION or base
                # pol_replace was already sanity checked, no need to check again
                if d in pol_dirs_sans_base and f in self.pol_replace:
                    self.policy_files[f] = [ full_path ]
               
                elif f in self.pol_union or d in self.base_policy:
                    self.policy_files[f].append(full_path)
        
        print("Generating file mapping complete")
         
    def __str__(self):
        '''
        To String function for debugging
        '''
        s = "BOARD_SEPOLICY_DIRS: " + str(self.pol_dirs) + "\n"
        s += "BOARD_SEPOLICY_UNION: " + str(self.pol_union) + "\n"
        s += "BOARD_SEPOLICY_REPLACE: " + str(self.pol_replace) + "\n"
        
        for k in self.policy_files:
            s += k + " : " + str(self.policy_files[k]) + "\n"
        
        return s

    def compile(self):
        pass
        

class SEPolicyBuilder(SEBuilder):
    
    # All regexp in this list get sent to be "anchorfy'd" This way mls doesn't have multiple matches, etc.
    compile_order = Utils.anchorfy("security_classes initial_sids access_vectors global_macros mls_macros mls policy_capabilities te_macros attributes \S*\.te roles users initial_sid_contexts fs_use genfs_contexts port_contexts").split()
    
    def __init__(self, *inputs, **kw):
        super(SEPolicyBuilder, self).__init__(*inputs, **kw)
        
    def compile(self):
        
        compile_policy_list = ""
        
        # Use the compile order list to start making in an order list of policy files
        # The key in this list could be a regular expression as well.
        for key in SEPolicyBuilder.compile_order:
            
            # Search for all policy file keys for that build order key
            r = re.compile(key)
            policy_file_keys = filter(r.match, self.policy_files)
            
            # For each policy file key in the build file keys that go there...
            s = Utils.flatten(([ self.policy_files[k] for k in policy_file_keys ]))
            compile_policy_list += " ".join(s) + " "

        # From Android.mk for sepolicy
        # m4 -D mls_num_sens=$(PRIVATE_MLS_SENS) -D mls_num_cats=$(PRIVATE_MLS_CATS) -s $^ > $@
        cmd = "m4 -D mls_num_sens=" + self.mls_sens + " -D mls_num_cats=" + self.mls_cats + " -s " + compile_policy_list +" > policy.conf"
        subprocess.call(cmd, shell=True)
        
        # From Android.mk for sepolicy
        cmd = "checkpolicy -M -c " + self.policy_vers + " -o sepolicy policy.conf"
        subprocess.call(cmd, shell=True)

class SEFileContextsBuilder(SEBuilder):
    
    file_context_key = "file_contexts"
    
    def __init__(self, *inputs, **kw):
        super(SEFileContextsBuilder, self).__init__(*inputs, **kw)
        
    def compile(self):
        
        compile_policy_list = ""
        
        # For each policy file key in the build file keys that go there...
        compile_policy_list += " ".join(self.policy_files[SEFileContextsBuilder.file_context_key]) + " "

        # From Android.mk for sepolicy
        # m4 -s $(ALL_FC_FILES) > $@
        # checkfc $(TARGET_ROOT_OUT)/sepolicy $@
        cmd = "m4 -s " + compile_policy_list +" > file_contexts"
        subprocess.call(cmd, shell=True)
        
        cmd = "checkfc sepolicy file_contexts"
        subprocess.call(cmd, shell=True)


class SESeappContextsBuilder(SEBuilder):
    
    check_seapp_key = "seapp_contexts"
    
    def __init__(self, *inputs, **kw):
        super(SESeappContextsBuilder, self).__init__(*inputs, **kw)
    
    def _order(self, x):
        cnt = 0
        for d in self.pol_dirs:
            if d in x and d not in self.base_policy: 
                return cnt
            elif d in self.base_policy:
                return len(self.pol_dirs) + 1
            cnt = cnt + 1
        return -1
    
    def compile(self):
        
        compile_policy_list = ""
        
        # This is a little bit tricky. Order matters in the seapp_contexts
        # concatenation. You should always ensure the reference policy file
        # goes last, otherwise honor the order in SEPOLICY_DIRS
        tmp = self.policy_files[SESeappContextsBuilder.check_seapp_key]
        seapp_context_file_list = sorted(tmp, key=self._order)

        # seapp_context_file_list.revers()
        # For each policy file key in the build file keys that go there...
        compile_policy_list += " ".join(seapp_context_file_list) + " "
	
        cmd = "m4 -s " + compile_policy_list +" > seapp_contexts.tmp"
        subprocess.call(cmd, shell=True)
        
        cmd = "checkseapp -p sepolicy -o seapp_contexts seapp_contexts.tmp"
        subprocess.call(cmd, shell=True)

class SEPropertyContextsBuilder(SEBuilder):
    
    property_contexts_key = "property_contexts"
    
    def __init__(self, *inputs, **kw):
        super(SEPropertyContextsBuilder, self).__init__(*inputs, **kw)
       
    def compile(self):
        
        compile_policy_list = ""
        
        # For each policy file key in the build file keys that go there...
        compile_policy_list += " ".join(self.policy_files[SEPropertyContextsBuilder.property_contexts_key]) + " "

        # From Android.mk for sepolicy
        # m4 -s $(ALL_FC_FILES) > $@
        # checkfc $(TARGET_ROOT_OUT)/sepolicy $@
        cmd = "m4 -s " + compile_policy_list +" > property_contexts"
        subprocess.call(cmd, shell=True)

def main():

    # Typically this will be set to the top of your ANDROID directory.
    ROOT = os.environ.get('SEPOLICY_ROOT') if os.environ.get('SEPOLICY_ROOT') != None else os.getcwd()
    
    # This is order sensitive for some build tools, like check_seapp!
    BOARD_SEPOLICY_DIRS = set(os.environ.get('BOARD_SEPOLICY_DIRS').split() if os.environ.get('BOARD_SEPOLICY_DIRS') != None else [])
    BOARD_SEPOLICY_REPLACE = set(os.environ.get('BOARD_SEPOLICY_REPLACE').split() if os.environ.get('BOARD_SEPOLICY_REPLACE') != None else [])
    BOARD_SEPOLICY_UNION = set(os.environ.get('BOARD_SEPOLICY_UNION').split() if os.environ.get('BOARD_SEPOLICY_UNION') != None else [])
    
    # Advanced features, leaving these unset is typically OK
    POLICYVERS = os.environ.get('POLICYVERS') if os.environ.get('POLICYVERS') != None else 24
    MLS_SENS = os.environ.get('MLS_SENS') if os.environ.get('MLS_SENS') != None else 1
    MLS_CATS = os.environ.get('MLS_CATS') if os.environ.get('MLS_CATS') != None else 1024
    BASE_SEPOLICY = os.environ.get('BASE_POLICY') if os.environ.get('BASE_POLICY') != None else "external/sepolicy"

    print("Starting policy build")
    # Build the policy first
    se_policy = SEPolicyBuilder(ROOT, BOARD_SEPOLICY_DIRS, BASE_SEPOLICY, BOARD_SEPOLICY_UNION, BOARD_SEPOLICY_REPLACE, MLS_CATS, MLS_SENS, POLICYVERS)
    print(se_policy)
    
    print("Copiling policy")
    se_policy.compile()
    print("Copiling policy done")
    # Then build the file contexts
    print("Creating file contexts")
    se_file_contexts = SEFileContextsBuilder(ROOT, BOARD_SEPOLICY_DIRS, BASE_SEPOLICY, BOARD_SEPOLICY_UNION, BOARD_SEPOLICY_REPLACE, MLS_CATS, MLS_SENS, POLICYVERS)
    se_file_contexts.compile()
    print("Creating file contexts done")
    print("Creating seapp contexts")
    se_seapp_contexts = SESeappContextsBuilder(ROOT, BOARD_SEPOLICY_DIRS, BASE_SEPOLICY, BOARD_SEPOLICY_UNION, BOARD_SEPOLICY_REPLACE, MLS_CATS, MLS_SENS, POLICYVERS)
    se_seapp_contexts.compile()
    print("Creating seapp contexts done")
    print("Creating property contexts")
    se_property_contexts = SEPropertyContextsBuilder(ROOT, BOARD_SEPOLICY_DIRS, BASE_SEPOLICY, BOARD_SEPOLICY_UNION, BOARD_SEPOLICY_REPLACE, MLS_CATS, MLS_SENS, POLICYVERS)
    se_property_contexts.compile()
    print("Creating property contexts done")
    print("Exiting...")

if __name__ == "__main__":
    main()
