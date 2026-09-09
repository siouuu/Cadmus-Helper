import json
from datetime import datetime

def get_color(course_type):
    colors = {
        "Cyber Range": "primary",
        "Serious Game": "success",
        "Table Top Exercise": "danger",
        "Malware Analysis & Reverse Engineering": "info",
        "Malware Analysis": "info",
        "Bootcamp": "warning"
    }
    return colors.get(course_type, "secondary")

def parse_date(date_str):
    if not date_str or date_str.upper() == "TBA":
        return datetime.max
    try:
        return datetime.strptime(date_str, "%d/%m/%y")
    except ValueError:
        return datetime.max

def format_display_date(date_str):
    if not date_str or date_str.upper() == "TBA":
        return date_str
    try:
        d = datetime.strptime(date_str, "%d/%m/%y")
        return d.strftime("%d/%m/%Y")
    except ValueError:
        return date_str

def format_deadline(date_str):
    if not date_str or date_str.upper() == "TBA":
        return date_str
    try:
        d = datetime.strptime(date_str, "%d/%m/%y")
        return d.strftime("%d %B %Y")
    except ValueError:
        return date_str

def format_session_id(session_id):
    if not session_id:
        return ""
    parts = session_id.split('-')
    if len(parts) >= 3:
        z = parts[-1]
        y = parts[-2].zfill(2)
        x = '-'.join(parts[:-2])
        return f"{x}-{y} (#{z})"
    return session_id

def generate_card(course, status):
    color = get_color(course.get("course_type", ""))
    
    if status == "ACTIVE":
        status_badge = '<span class="badge cadmus-badge-open text-uppercase">Active</span>'
    elif status == "UPCOMING":
        status_badge = '<span class="badge bg-warning text-dark text-uppercase">Upcoming</span>'
    else:
        status_badge = '<span class="badge bg-secondary text-uppercase">Closed</span>'

    enrol_open = False
    if status in ["ACTIVE", "UPCOMING"]:
        deadline_date = parse_date(course.get("enrolment_end_date", ""))
        if deadline_date != datetime.max:
            deadline_date = deadline_date.replace(hour=23, minute=59, second=59)
            if datetime.now() <= deadline_date:
                enrol_open = True

    if enrol_open:
        btn_class = "btn-primary"
        btn_href = f'href="{course.get("enrolment_url", "#")}" target="_blank" rel="noopener"'
        btn_attr = ''
    else:
        btn_class = "btn-secondary disabled"
        btn_href = 'href="#"'
        btn_attr = 'aria-disabled="true" tabindex="-1"'

    start_disp = format_display_date(course.get("course_start_date", ""))
    end_disp = format_display_date(course.get("course_end_date", ""))
    session_disp = f"{start_disp} - {end_disp}" if start_disp and end_disp else course.get("course_start_date", "")
    deadline_disp = format_deadline(course.get("enrolment_end_date", ""))
    formatted_id = format_session_id(course.get("training_session_id", ""))

    return f'''
    <div class="col-12 col-md-6 col-lg-4 px-2 mb-4">
      <div class="card cadmus-course-card h-100 shadow-sm">
        <div class="cadmus-accent bg-{color}" aria-hidden="true"> </div>
        <div class="card-body d-flex flex-column">
          <div class="mb-3">
            <span class="badge bg-{color} text-uppercase me-1">{course.get("course_type", "")}</span>
            {status_badge}
          </div>
          <h3 class="card-title fw-bold mb-3"><a href="{course.get("course_url", "#")}" target="_blank" rel="noopener">{course.get("course_title", "")}</a></h3>
          <div class="mb-4 small">
            <div class="mb-1"><span class="text-muted">Session ID:</span> <strong>{formatted_id}</strong></div>
            <div><span class="text-muted">Training Session:</span> <strong>{session_disp}</strong></div>
          </div>
          <div class="cadmus-meta mt-auto">
            <span class="cadmus-date small">
              <span class="text-muted">Enrolment deadline:</span> <strong>{deadline_disp}</strong>
            </span>
            <a class="btn {btn_class} cadmus-mini-register" {btn_href} {btn_attr}>Enrol</a>
          </div>
        </div>
      </div>
    </div>
    '''

def main():
    with open('courses.json', 'r', encoding='utf-8') as f:
        courses = json.load(f)

    courses.sort(key=lambda x: parse_date(x.get("course_start_date", "")))

    now = datetime.now()
    active = []
    upcoming = []
    closed = []

    for c in courses:
        start = parse_date(c.get("course_start_date", ""))
        end = parse_date(c.get("course_end_date", ""))
        if end != datetime.max:
            end = end.replace(hour=23, minute=59, second=59)
            
        if now < start:
            upcoming.append(c)
        elif start <= now <= end:
            active.append(c)
        else:
            closed.append(c)

    html_output = '''
<style>
.cadmus-training-grid { max-width: 1200px; margin: 0 auto; color: var(--bs-body-color, inherit); font-family: inherit; }
.cadmus-training-grid .cadmus-course-card { overflow: hidden; background-color: var(--bs-card-bg, var(--bs-body-bg)); color: var(--bs-body-color, inherit); border: 1px solid var(--bs-border-color); border-radius: .5rem; }
.cadmus-training-grid .cadmus-accent { height: 3px; }
.cadmus-training-grid .card-body { padding: 1rem; }
.cadmus-training-grid .card-title { color: var(--bs-body-color, inherit); font-size: .98rem; line-height: 1.35; }
.cadmus-training-grid .card-title a { color: inherit; text-decoration: none; }
.cadmus-training-grid .card-title a:hover { text-decoration: underline; }
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

    html_output += '<h4 class="mb-4 text-dark border-bottom pb-2 fw-bold">Upcoming Training Sessions:</h4>\n'
    html_output += '<div class="row justify-content-start mx-n2 mb-5">\n'
    if upcoming:
        for c in upcoming:
            html_output += generate_card(c, "UPCOMING")
    else:
        html_output += '''
        <div class="col-12 px-2">
          <div class="p-4 bg-light rounded text-center text-muted border" style="background-color: var(--bs-secondary-bg, #f8f9fa);">
            <p class="mb-0">New trainings will be announced shortly. Stay tuned!</p>
          </div>
        </div>
        '''
    html_output += '</div>\n'

    html_output += '<h4 class="mb-4 text-dark border-bottom pb-2 fw-bold">Active Training Sessions:</h4>\n'
    html_output += '<div class="row justify-content-start mx-n2 mb-5">\n'
    if active:
        for c in active:
            html_output += generate_card(c, "ACTIVE")
    else:
        html_output += '''
        <div class="col-12 px-2">
          <div class="p-4 bg-light rounded text-center text-muted border" style="background-color: var(--bs-secondary-bg, #f8f9fa);">
            <p class="mb-0">No active training sessions available at the moment.</p>
          </div>
        </div>
        '''
    html_output += '</div>\n'

    if closed:
        html_output += '<h4 class="mb-4 text-dark border-bottom pb-2 fw-bold">Closed Training Sessions:</h4>\n'
        html_output += '<div class="row justify-content-start mx-n2 mb-5">\n'
        for c in closed:
            html_output += generate_card(c, "CLOSED")
        html_output += '</div>\n'

    html_output += '</div>'

    with open('output.html', 'w', encoding='utf-8') as f:
        f.write(html_output)
        
if __name__ == "__main__":
    main()