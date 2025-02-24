from django.http import HttpResponse

def home(request):
    """Render the Weather API home page as a simple HTML response.

    Returns an HTML page with links to the Swagger UI, API specification, and GitHub repository.

    Args:
        request (rest_framework.request.Request): The incoming HTTP request object.

    Returns:
        rest_framework.response.Response: An HTTP response with the rendered HTML content.
    """
    html_content = """
    <h1>Welcome to the Weather API</h1>
    <ul>
        <li>Test the API using <a href="/api/schema/swagger-ui/">Swagger UI</a></li>
        <li>Download the API specification: <a href="/api/schema/">API specification</a></li>
        <li>For more details, check out our <a href="https://github.com/WeatherCrew/weather-api">GitHub Repository</a></li>
    </ul>
    """
    return HttpResponse(html_content)
