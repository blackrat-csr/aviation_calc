from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import math
from .models import CalculationHistory

def home(request):
    """Home page with navigation to different calculators"""
    return render(request, 'calculator/home.html')

@csrf_exempt
def wind_triangle(request):
    """Wind Triangle Calculator"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract inputs
            true_airspeed = float(data.get('true_airspeed', 0))
            true_course = float(data.get('true_course', 0))
            wind_direction = float(data.get('wind_direction', 0))
            wind_speed = float(data.get('wind_speed', 0))
            
            # Convert degrees to radians for calculations
            tc_rad = math.radians(true_course)
            wd_rad = math.radians(wind_direction)
            
            # Calculate wind correction angle and ground speed
            # Using standard aviation wind triangle formulas
            wind_angle = wd_rad - tc_rad
            drift_angle = math.asin((wind_speed * math.sin(wind_angle)) / true_airspeed)
            ground_speed = true_airspeed * math.cos(drift_angle) - wind_speed * math.cos(wind_angle)
            
            # Calculate magnetic heading (true course + drift angle)
            magnetic_heading = true_course + math.degrees(drift_angle)
            
            # Normalize heading to 0-360 range
            if magnetic_heading < 0:
                magnetic_heading += 360
            elif magnetic_heading >= 360:
                magnetic_heading -= 360
                
            results = {
                'drift_angle': round(math.degrees(drift_angle), 2),
                'magnetic_heading': round(magnetic_heading, 2),
                'ground_speed': round(ground_speed, 2),
            }
            
            # Save to history
            CalculationHistory.objects.create(
                calculation_type='wind_triangle',
                inputs=data,
                results=results
            )
            
            return JsonResponse({'success': True, 'results': results})
            
        except (ValueError, TypeError, ZeroDivisionError) as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'calculator/wind_triangle.html')

@csrf_exempt
def great_circle(request):
    """Great Circle Distance Calculator"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract coordinates
            lat1 = math.radians(float(data.get('lat1', 0)))
            lon1 = math.radians(float(data.get('lon1', 0)))
            lat2 = math.radians(float(data.get('lat2', 0)))
            lon2 = math.radians(float(data.get('lon2', 0)))
            
            # Earth's radius in nautical miles
            R = 3440.065
            
            # Haversine formula
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            distance = R * c
            
            # Initial bearing calculation
            y = math.sin(dlon) * math.cos(lat2)
            x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
            initial_bearing = math.degrees(math.atan2(y, x))
            
            # Normalize bearing to 0-360 range
            if initial_bearing < 0:
                initial_bearing += 360
                
            results = {
                'distance': round(distance, 2),
                'initial_bearing': round(initial_bearing, 2),
            }
            
            # Save to history
            CalculationHistory.objects.create(
                calculation_type='great_circle',
                inputs=data,
                results=results
            )
            
            return JsonResponse({'success': True, 'results': results})
            
        except (ValueError, TypeError) as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'calculator/great_circle.html')

@csrf_exempt
def rhumb_line(request):
    """Rhumb Line Distance and Bearing Calculator"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract coordinates
            lat1 = math.radians(float(data.get('lat1', 0)))
            lon1 = math.radians(float(data.get('lon1', 0)))
            lat2 = math.radians(float(data.get('lat2', 0)))
            lon2 = math.radians(float(data.get('lon2', 0)))
            
            # Earth's radius in nautical miles
            R = 3440.065
            
            # Calculate delta latitude and longitude
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            # Adjust for crossing 180° meridian
            if abs(dlon) > math.pi:
                if dlon > 0:
                    dlon = -(2 * math.pi - dlon)
                else:
                    dlon = (2 * math.pi + dlon)
            
            # Calculate delta phi (mercator projection)
            dphi = math.log(math.tan(lat2/2 + math.pi/4) / math.tan(lat1/2 + math.pi/4))
            
            # Calculate bearing
            if abs(dphi) > 10e-12:
                q = dlat / dphi
            else:
                q = math.cos(lat1)
            
            bearing = math.atan2(dlon, dphi)
            distance = math.sqrt(dlat**2 + q**2 * dlon**2) * R
            
            # Convert bearing to degrees and normalize
            bearing_deg = math.degrees(bearing)
            if bearing_deg < 0:
                bearing_deg += 360
                
            results = {
                'distance': round(distance, 2),
                'bearing': round(bearing_deg, 2),
            }
            
            # Save to history
            CalculationHistory.objects.create(
                calculation_type='rhumb_line',
                inputs=data,
                results=results
            )
            
            return JsonResponse({'success': True, 'results': results})
            
        except (ValueError, TypeError) as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'calculator/rhumb_line.html')

def history(request):
    """Display calculation history"""
    calculations = CalculationHistory.objects.all().order_by('-created_at')[:50]
    return render(request, 'calculator/history.html', {'calculations': calculations})
