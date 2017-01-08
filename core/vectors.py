from mako.template import Template
from core.weexceptions import DevException, ModuleError
from core import modules
from core import utilities
from core import messages
from core.utilities import Os

class Vectors(list):

    def __init__(self, session, module_name):

        self.session = session
        self.module_name = module_name

        list.__init__(self)

    def find_first_result(self, names = [ '' ], arguments = {}, condition = None, store_result = False, store_name = ''):
        """ Execute all the vectors returning the result matching the given condition.

        Return the name and the result of the first vector that gives the response that satisfy
        a certain condition.

        With unspecified names, apply to all the vectors. Optionally store results.

        Args:
            names: The names lists of vectors to execute.
            arguments: The dictionary of arguments to format the vectors with.
            condition: The function to verify the result condition is verified (returns
                a true value). This has to be a function.
            store_result: Store as result. This has to be a boolean.
            store_name: Store the found vector name as argument. This must contain a string
            with the argument.

        Returns:
            A tuple with the vector results in the `( vector_name, result )` form.

        """

        if not callable(condition):
            raise DevException(messages.vectors.wrong_condition_type)
        if not isinstance(store_name, str):
            raise DevException(messages.vectors.wrong_store_name_type)

        for vector in self:

            if not self._os_match(vector.target): continue

            if not any(x in vector.name for x in names): continue

            result = vector.run(arguments)

            if condition(result):

                if store_result:
                    self.session[self.module_name]['results'][vector.name] = result
                if store_name:
                    self.session[self.module_name]['stored_args'][store_name] = vector.name

                return vector.name, result

        return None, None

    def get_result(self, name, arguments = {}, store_result = ''):
        """Run one vector.

        Run the vector with specified name. Optionally store results.

        Args:
            name: The name string of vector to execute.
            arguments: The dictionary of arguments to format the vectors with.
            store_result: Store as result. This has to be a boolean.

        Returns:
            An object with the vector execution result.

        """

        vector = self.get_by_name(name)

        if vector and self._os_match(vector.target):
            result = vector.run(arguments)

            if store_result:
                self.session[self.module_name]['results'][name] = result

            return result


    def get_results(self, names = [ '' ], arguments = {}, results_to_store = [ ]):
        """Run all the vectors.

        Returns a dictionary with the vector names as keys and the results as arguments.
        With unspecified names, execute all the vectors. Optionally store results.

        Args:
            names: A list of names of vectors to execute.
            arguments: The dictionary of arguments to format the vectors with.
            results_to_store: The names lists of vectors of which save the
                returned result.

        Returns:
            A dictionary with all the vector results in the
            `{ vector_name : result }` form.
        """

        response = {}

        for vector in self:

            if not self._os_match(vector.target): continue

            if not any(x in vector.name for x in names): continue

            response[vector.name] = vector.run(arguments)

            if not any(x in vector.name for x in results_to_store): continue

            self.session[self.module_name]['results'][vector.name] = response[vector.name]

        return response

    def _os_match(self, os):
        """Check if vector os is compatible with the remote os"""

        os_string = self.session['system_info']['results'].get('os')

        # If os_string is not set, just return True and continue
        if not os_string: return True

        os_current = s.WIN if os_string.lower().startswith('win') else Os.NIX

        return os in (os_current, Os.ANY)

    def get_by_name(self, name):
        return next(v for v in self if v.name == name)

    def get_names(self):
        return [ v.name for v in self ]
