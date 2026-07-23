import json
from datetime import datetime

def get_color(course_type):
    colors = {
        "Cyber Range": "primary",
        "Serious Game": "success",
        "Table-Top Exercise": "danger",
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
        status_badge = '<span class="badge cadmus-badge-open text-uppercase">Active</span>'
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
          <h3 class="card-title fw-bold mb-3">{course["title"]}</h3>
          <div class="mb-4 small">
            <div class="mb-1"><span class="text-muted">Course ID:</span> <strong>{course["id"]}</strong></div>
            <div><span class="text-muted">Training Session:</span> <strong>{course["session"]}</strong></div>
          </div>
          <div class="cadmus-meta mt-auto">
            <span class="cadmus-date small">
              <span class="text-muted">Registration deadline:</span> <strong>{course["deadline"]}</strong>
            </span>
            <a class="btn {btn_class} cadmus-mini-register" {btn_href} {btn_attr}>Register</a>
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

    html_output = '''
<style>
.cadmus-training-grid { max-width: 1200px; margin: 0 auto; color: var(--bs-body-color, inherit); font-family: inherit; }
.cadmus-training-grid .cadmus-course-card { overflow: hidden; background-color: var(--bs-card-bg, var(--bs-body-bg)); color: var(--bs-body-color, inherit); border: 1px solid var(--bs-border-color); border-radius: .5rem; }
.cadmus-training-grid .cadmus-accent { height: 3px; }
.cadmus-training-grid .card-body { padding: 1rem; }
.cadmus-training-grid .card-title { color: var(--bs-body-color, inherit); font-size: .98rem; line-height: 1.35; }
.cadmus-training-grid .badge { font-size: .65rem; font-weight: 600; letter-spacing: .035em; padding: .32rem .48rem; }
.cadmus-training-grid .cadmus-badge-open { color: #146c43; background-color: #d1e7dd; border: 1px solid #a3cfbb; }
.cadmus-training-grid .cadmus-meta { display: flex; align-items: center; gap: .25rem; background-color: var(--bs-secondary-bg, #f8f9fa); border: 1px solid var(--bs-border-color); border-radius: .375rem; padding: .42rem .5rem; }
.cadmus-training-grid .cadmus-date { min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cadmus-training-grid .cadmus-date strong { color: var(--bs-body-color, inherit); }
.cadmus-training-grid .cadmus-mini-register { margin-left: auto; flex: 0 0 auto; width: auto; min-width: 0; padding: .14rem .42rem; font-size: .72rem; line-height: 1.15; font-weight: 600; border-radius: .25rem; }
.cadmus-training-grid .text-muted { color: var(--bs-secondary-color, #6c757d) !important; }
</style>
<div class="cadmus-training-grid py-4">
'''

    html_output += '<h4 class="mb-4 text-dark border-bottom pb-2 fw-bold">Coming Soon</h4>\n'
    html_output += '<div class="row justify-content-start mx-n2 mb-5">\n'
    if coming:
        for c in coming:
            html_output += generate_card(c)
    else:
        html_output += '''
        <div class="col-12 px-2">
          <div class="p-4 bg-light rounded text-center text-muted border" style="background-color: var(--bs-secondary-bg, #f8f9fa);">
            <p class="mb-0">New bootcamps and training modules will be announced shortly. Stay tuned!</p>
          </div>
        </div>
        '''
    html_output += '</div>\n'

    if active:
        html_output += '<h4 class="mb-4 text-dark border-bottom pb-2 fw-bold">Active Courses</h4>\n'
        html_output += '<div class="row justify-content-start mx-n2 mb-5">\n'
        for c in active:
            html_output += generate_card(c)
        html_output += '</div>\n'

    if closed:
        html_output += '<h4 class="mb-4 text-dark border-bottom pb-2 fw-bold">Closed Courses</h4>\n'
        html_output += '<div class="row justify-content-start mx-n2 mb-5">\n'
        
        for c in closed[:3]:
            html_output += generate_card(c)
            
        if len(closed) > 3:
            html_output += '</div>\n'
            html_output += '<div class="text-center mb-4">\n'
            html_output += '<button class="btn btn-outline-secondary px-4" type="button" data-bs-toggle="collapse" data-bs-target="#moreClosedCourses" aria-expanded="false" aria-controls="moreClosedCourses">Show More Closed Courses</button>\n'
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