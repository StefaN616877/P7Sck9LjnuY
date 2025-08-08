# 代码生成时间: 2025-08-09 07:12:14
import tornado.ioloop
import tornado.web

"""
A simple Tornado web service that provides sorting algorithms implementation.
"""

class SortingHandler(tornado.web.RequestHandler):
    """
    Request handler for sorting algorithms.
    """
    def get(self):
        """
        Handles GET requests to provide sorting functionality.
        """
        try:
            # Retrieve the list of numbers to sort from the query parameters
            numbers = self.get_query_argument('numbers', None)
            if numbers is None:
                self.write({'error': 'No numbers provided.'})
                return
            
            # Convert the string of numbers to a list of integers
            numbers = [int(n) for n in numbers.split(',')]
            
            # Sort the numbers using a sorting algorithm
            sorted_numbers = self.sort_numbers(numbers)
            
            # Return the sorted list as a JSON response
            self.write({'sorted_numbers': sorted_numbers})
        except ValueError:
            self.write({'error': 'Invalid input. Please provide a comma-separated list of numbers.'})
        except Exception as e:
            self.write({'error': str(e)})

    def sort_numbers(self, numbers):
        """
        Sorts a list of numbers using the bubble sort algorithm.
        """
        n = len(numbers)
        for i in range(n):
            for j in range(0, n-i-1):
                if numbers[j] > numbers[j+1]:
                    numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
        return numbers

def make_app():
    """
    Creates a Tornado application.
    """
    return tornado.web.Application(
        [('/sort', SortingHandler)],
        debug=True,
    )

if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    print('Sorting service is running on http://localhost:8888')
    tornado.ioloop.IOLoop.current().start()