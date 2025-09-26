# Aviation Calculator

A Django web application for performing essential aviation calculations including wind triangle, great circle, and rhumb line navigation.

## Origin

Vibe Coded by github copilot cli from prompt:

```
Please create simple django html/templates project for web application allowing user to do aviation calculations. Start with wind triangle, great circle and rhumb line. Use uv to manage project dependencies and virtual environment.
```

## Features

### 🌬️ Wind Triangle Calculator
- Calculate wind correction angle, magnetic heading, and ground speed
- Takes true airspeed, true course, wind direction, and wind speed as inputs
- Essential for flight planning and navigation

### 🌍 Great Circle Calculator  
- Calculate shortest distance and initial bearing between two points on Earth
- Uses the Haversine formula for precise great circle navigation
- Results in nautical miles and degrees

### 🧭 Rhumb Line Calculator
- Calculate constant bearing navigation distance and course
- Useful for simple navigation with constant compass heading
- Shows the trade-off between simplicity and distance vs great circle

### 📊 Calculation History
- Automatically saves all calculations with timestamps
- View past calculations with inputs and results
- Organized by calculation type with color coding

## Installation
## Project Structure

## API Reference

All endpoints accept POST requests for calculation (with form or JSON data) and GET for HTML UI.

| Endpoint              | Method | Description                                      | POST Params (form/JSON)                | Response (HTMX/JSON) |
|----------------------|--------|--------------------------------------------------|----------------------------------------|----------------------|
| `/`                  | GET    | Home page, navigation                            | –                                      | HTML                 |
| `/wind-triangle/`    | GET    | Wind triangle calculator form                    | –                                      | HTML                 |
| `/wind-triangle/`    | POST   | Calculate wind triangle                          | true_airspeed, true_course, wind_direction, wind_speed | HTML fragment (HTMX) or JSON |
| `/great-circle/`     | GET    | Great circle calculator form                     | –                                      | HTML                 |
| `/great-circle/`     | POST   | Calculate great circle distance & bearing        | lat1, lon1, lat2, lon2                 | HTML fragment (HTMX) or JSON |
| `/rhumb-line/`       | GET    | Rhumb line calculator form                       | –                                      | HTML                 |
| `/rhumb-line/`       | POST   | Calculate rhumb line distance & bearing          | lat1, lon1, lat2, lon2                 | HTML fragment (HTMX) or JSON |
| `/history/`          | GET    | Calculation history                              | –                                      | HTML                 |

### Example POST (JSON)


```
POST /great-circle/
Content-Type: application/json
{
   "lat1": 50.1,
   "lon1": 14.4,
   "lat2": 48.9,
   "lon2": 2.4
}
```

#### curl
```sh
curl -X POST http://127.0.0.1:8000/great-circle/ \
  -H "Content-Type: application/json" \
  -d '{"lat1": 50.1, "lon1": 14.4, "lat2": 48.9, "lon2": 2.4}'
```

#### PowerShell
```powershell
$body = @{ lat1=50.1; lon1=14.4; lat2=48.9; lon2=2.4 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/great-circle/" -Method Post -ContentType "application/json" -Body $body
```

### Example POST (form/HTMX)


```
POST /great-circle/
Content-Type: application/x-www-form-urlencoded
lat1=50.1&lon1=14.4&lat2=48.9&lon2=2.4
```

### Example POST (JSON) for wind_triangle


```
POST /wind-triangle/
Content-Type: application/json
{
   "true_airspeed": 120,
   "true_course": 90,
   "wind_direction": 180,
   "wind_speed": 20
}
```

#### curl
```sh
curl -X POST http://127.0.0.1:8000/wind-triangle/ \
   -H "Content-Type: application/json" \
   -d '{"true_airspeed": 120, "true_course": 90, "wind_direction": 180, "wind_speed": 20}'
```

#### PowerShell
```powershell
$body = @{ true_airspeed=120; true_course=90; wind_direction=180; wind_speed=20 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/wind-triangle/" -Method Post -ContentType "application/json" -Body $body
```

### Example POST (form/HTMX) for wind_triangle

```
POST /wind-triangle/
Content-Type: application/x-www-form-urlencoded
true_airspeed=120&true_course=90&wind_direction=180&wind_speed=20
```

### Example POST (JSON) for rhumb_line


```
POST /rhumb-line/
Content-Type: application/json
{
   "lat1": 50.1,
   "lon1": 14.4,
   "lat2": 48.9,
   "lon2": 2.4
}
```

#### curl
```sh
curl -X POST http://127.0.0.1:8000/rhumb-line/ \
   -H "Content-Type: application/json" \
   -d '{"lat1": 50.1, "lon1": 14.4, "lat2": 48.9, "lon2": 2.4}'
```

#### PowerShell
```powershell
$body = @{ lat1=50.1; lon1=14.4; lat2=48.9; lon2=2.4 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/rhumb-line/" -Method Post -ContentType "application/json" -Body $body
```

### Example POST (form/HTMX) for rhumb_line

```
POST /rhumb-line/
Content-Type: application/x-www-form-urlencoded
lat1=50.1&lon1=14.4&lat2=48.9&lon2=2.4
```

```
aviation-calculator/
├── aviationcalc/                # Django project config (settings, urls, wsgi, asgi)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── calculator/                  # Main Django app with all aviation calculators
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── models.py
│   ├── static/
│   │   └── calculator/
│   │       └── htmx.min.js
│   ├── templates/
│   │   └── calculator/
│   │       ├── base.html
│   │       ├── fragments/
│   │       │   ├── great_circle_fragment.html
│   │       │   ├── rhumb_line_fragment.html
│   │       │   └── wind_triangle_fragment.html
│   │       ├── great_circle.html
│   │       ├── history.html
│   │       ├── home.html
│   │       ├── rhumb_line.html
│   │       └── wind_triangle.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3                   # SQLite database
├── manage.py                    # Django management script
├── pyproject.toml               # Project dependencies (uv/poetry compatible)
├── uv.lock                      # uv lockfile
└── README.md
```
This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

1. Navigate to the project directory:
```bash
cd aviation-calculator
```

2. Install dependencies:
```bash
uv sync
```

3. Run database migrations:
```bash
uv run python manage.py migrate
```

4. Start the development server:
```bash
uv run python manage.py runserver
```

5. Open your browser to `http://127.0.0.1:8000`

## Usage

### Wind Triangle
1. Enter true airspeed in knots
2. Enter desired true course in degrees (0-359°)
3. Enter wind direction (where wind is coming from) in degrees
4. Enter wind speed in knots
5. Click "Calculate Wind Triangle" to get:
   - Drift angle (degrees)
   - Magnetic heading to fly (degrees) 
   - Ground speed (knots)

### Great Circle Navigation
1. Enter departure point latitude and longitude in decimal degrees
2. Enter destination point latitude and longitude in decimal degrees
3. Click "Calculate Great Circle" to get:
   - Shortest distance in nautical miles
   - Initial bearing in degrees

### Rhumb Line Navigation
1. Enter departure point latitude and longitude in decimal degrees
2. Enter destination point latitude and longitude in decimal degrees  
3. Click "Calculate Rhumb Line" to get:
   - Distance along constant bearing route in nautical miles
   - Constant bearing to maintain in degrees

## Technical Details

### Wind Triangle Calculations
Uses standard aviation formulas:
- Drift angle = arcsin((wind_speed × sin(wind_angle)) / true_airspeed)
- Ground speed = true_airspeed × cos(drift_angle) - wind_speed × cos(wind_angle)
- Magnetic heading = true_course + drift_angle

### Great Circle Calculations
Uses the Haversine formula:
- Distance = 2R × arcsin(√(sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)))
- Initial bearing = atan2(sin(Δlon) × cos(lat2), cos(lat1) × sin(lat2) - sin(lat1) × cos(lat2) × cos(Δlon))

### Rhumb Line Calculations
Uses loxodromic navigation formulas accounting for Mercator projection.

## Project Structure

```
aviation-calculator/
├── aviationcalc/           # Django project settings
├── calculator/             # Main calculator app
│   ├── models.py          # CalculationHistory model
│   ├── views.py           # Calculator logic and views
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin interface
│   └── templates/         # HTML templates
│       └── calculator/
│           ├── base.html
│           ├── home.html
│           ├── wind_triangle.html
│           ├── great_circle.html
│           ├── rhumb_line.html
│           └── history.html
├── manage.py              # Django management script
├── pyproject.toml         # uv/Python project configuration
└── README.md             # This file
```

## Dependencies

- Django 5.2.6 - Web framework
- Python 3.12+ - Programming language
- Bootstrap 5.1.3 - CSS framework (via CDN)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Future Enhancements

- [ ] Add more aviation calculations (fuel planning, weight & balance)
- [ ] Export calculation history to CSV/PDF
- [ ] Add unit conversions (metric/imperial)
- [ ] Mobile-responsive improvements
- [ ] User authentication and personal calculation history
- [ ] Interactive maps for great circle visualization
- [ ] API endpoints for programmatic access
