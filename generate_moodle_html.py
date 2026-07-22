import json
from datetime import datetime

def get_color(course_type):
    colors = {
        "Cyber Range": "primary",
        "Serious Game": "success",
        "Table-Top Exercise": "info",
        "Malware Analysis": "info",
        "Bootcamp": "warning"
    }
    return colors.get(course_type, "secondary")

def check_registration_open(deadline_str, status):
    if status != "ACTIVE":
        return False
    if deadline_str.upper() == "TBA":
        return False
    try:
        deadline_date = datetime.strptime(deadline_str, "%d %B %Y")
        deadline_date = deadline_date.replace(hour=23, minute=59, second=59)
        return datetime.now() <= deadline_date
    except ValueError:
        return False

def generate_card(course):
    status = course["status"]
    color = get_color(course["type"])
    
    if status == "ACTIVE":
        status_badge = '<span class="badge bg-success text-uppercase">Active</span>'
    elif status == "COMING SOON":
        status_badge = '<span class="badge bg-warning text-dark text-uppercase">Coming Soon</span>'
    else:
        status_badge = '<span class="badge bg-secondary text-uppercase">Closed</span>'

    registration_open = check_registration_open(course["deadline"], status)

    if registration_open:
        btn_class = "btn-primary"
        btn_href = f'href="{course.get("link", "#")}" target="_blank" rel="noopener"'
        btn_attr = ''
    else:
        btn_class = "btn-secondary disabled"
        btn_href = 'href="#"'
        btn_attr = 'aria-disabled="true" tabindex="-1"'

    return f'''
    <div class="col-12 col-md-6 col-lg-4 px-2 mb-4">
      <div class="card cadmus-course-card h-100 shadow-sm">
        <div class="cadmus-accent bg-{color}" aria-hidden="true"></div>
        <div class="card-body d-flex flex-column">
          <div class="mb-3">
            <span class="badge bg-{color} text-uppercase me-1">{course["type"]}</span>
            {status_badge}
          </div>
          <h5 class="card-title fw-bold mb-3">{course["title"]}</h5>
          <div class="mb-4 small">
            <div class="mb-1"><span class="text-muted">Course ID:</span> <strong>{course["id"]}</strong></div>
            <div><span class="text-muted">Training Session:</span> <strong>{course["session"]}</strong></div>
          </div>
          <div class="mt-auto bg-light p-2 rounded d-flex justify-content-between align-items-center">
            <span class="small text-muted">Registration deadline: <strong class="text-dark">{course["deadline"]}</strong></span>
            <a class="btn btn-sm {btn_class} cadmus-mini-register" {btn_href} {btn_attr}>Register</a>
          </div>
        </div>
      </div>
    </div>
    '''

def main():
    with open('courses.json', 'r', encoding='utf-8') as f:
        courses = json.load(f)

    active = [c for c in courses if c["status"] == "ACTIVE"]
    coming = [c for c in courses if c["status"] == "COMING SOON"]
    closed = [c for c in courses if c["status"] == "CLOSED"]

    html_output = '<div class="cadmus-training-sections py-3">\n'

    if active:
        html_output += '<h3 class="mb-3 text-success border-bottom pb-2">Active Courses</h3>\n'
        html_output += '<div class="row justify-content-start mx-n2 mb-5">\n'
        for c in active:
            html_output += generate_card(c)
        html_output += '</div>\n'

    if coming:
        html_output += '<h3 class="mb-3 text-warning border-bottom pb-2">Coming Soon</h3>\n'
        html_output += '<div class="row justify-content-start mx-n2 mb-5">\n'
        for c in coming:
            html_output += generate_card(c)
        html_output += '</div>\n'

    if closed:
        html_output += '<h3 class="mb-3 text-secondary border-bottom pb-2">Closed Courses</h3>\n'
        html_output += '<div class="row justify-content-start mx-n2 mb-5">\n'
        
        for c in closed[:3]:
            html_output += generate_card(c)
            
        if len(closed) > 3:
            html_output += '</div>\n'
            html_output += '<div class="text-center mb-4">\n'
            html_output += '<button class="btn btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#moreClosedCourses" aria-expanded="false" aria-controls="moreClosedCourses">Show More Closed Courses</button>\n'
            html_output += '</div>\n'
            html_output += '<div class="collapse" id="moreClosedCourses">\n'
            html_output += '<div class="row justify-content-start mx-n2 mb-5">\n'
            for c in closed[3:]:
                html_output += generate_card(c)
            html_output += '</div>\n</div>\n'
        else:
            html_output += '</div>\n'

    html_output += '</div>'

    with open('output.html', 'w', encoding='utf-8') as f:
        f.write(html_output)
        
if __name__ == "__main__":
    main()