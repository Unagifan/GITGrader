import base64
import os
import subprocess


class MetaMap:
    def __init__(self, path):
        self.path = path

    def map_concepts(self, concepts):
        '''
        Given a list [str2, str2, str3, ...], start a subprocess to transform list of strings to
         a dictionary of a list of UMLS concepts.
        :param concepts: [str1, str2, str3, ...]
        :return:Dict: {str1:list[UMLSConcept1, UMLSConcept2, UMLSConcept3, ...]}
        '''
        # Make subprocess call, capture output
        result_dict = dict()
        for concept in concepts:
            if concept not in result_dict:
                p = subprocess.Popen([os.path.join(self.path,'metamaplite.bat'),'--pipe'],stdout=subprocess.PIPE,stdin=subprocess.PIPE,
                                     stderr= subprocess.PIPE,cwd=self.path)
                stdout_data = p.communicate(bytes(concept,encoding='utf-8'))
                result_dict[concept] = self._build_umls_concepts(str(stdout_data[0],'utf-8'))
        return result_dict

    def _build_umls_concepts(self, output):
        '''
        Given raw input from the subprocess call to metamap, return a list of concept dictionaries:
        list[{'text':_, 'sem_class':_, 'start':_, 'end':_ 'cui':_},
             {'text':_, 'sem_class':_, 'start':_, 'end':_ 'cui':_},
             ...
            ]
        :param output: text output from metamap subcall
        :return: list of umls concept dictionaries
        '''
        concept_dict_list = list()
        individual_concepts = output.split('\n')
        if len(individual_concepts) == 45:
            concept = individual_concepts[-2]
        elif len(individual_concepts) == 44:
            concept = individual_concepts[-1]
        else:
            return "Metamap cannot recognize this term"
        if concept != "":
            concept_dict = dict()
            items = concept.split("|")
            concept_dict['desc'] = items[3]
            concept_dict['sem_class'] = items[5].lstrip('[').rstrip(']')
            concept_dict['start'] = int(items[7].split("/")[0])
            concept_dict['end'] = int(items[7].split("/")[1]) + int(items[7].split("/")[0])
            concept_dict['cui'] = items[4]
            concept_dict_list.append(concept_dict)
        return concept_dict_list


