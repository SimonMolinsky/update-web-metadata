import pickle

from pyosmeta import ProcessIssues

with open("../token.pickle", "rb") as f:
    API_TOKEN = pickle.load(f)

# result.status_code in [200, 302]:
# TODO:  I get key errors and name errors when i hit api limits
# Would be good to track API return responses / figure out how long I need to wait
# so it doesn't just fail. how does that get setup?
# TODO: add date issue closed as well - can get that from API maybe?
issueProcess = ProcessIssues(
    org="pyopensci",
    repo_name="software-submission",
    label_name="6/pyOS-approved 🚀🚀🚀",
    API_TOKEN=API_TOKEN,
)

# Get all issues for approved packages
issues = issueProcess.return_response("lwasser")
review = issueProcess.parse_issue_header(issues, 12)

# Get list of github API endpoint for each accepted package
all_repo_endpoints = issueProcess.get_repo_endpoints(review)

# Send a GET request to the API endpoint and include a user agent header
gh_stats = [
    "name",
    "description",
    "homepage",
    "created_at",
    "stargazers_count",
    "watchers_count",
    "stargazers_count",
    "forks",
    "open_issues_count",
    "forks_count",
]

# Get gh metadata for each package submission
all_repo_meta = {}
for package_name in all_repo_endpoints.keys():
    print(package_name)
    package_api = all_repo_endpoints[package_name]
    all_repo_meta[package_name] = issueProcess.get_repo_meta(package_api, gh_stats)

    all_repo_meta[package_name]["contrib_count"] = issueProcess.get_repo_contribs(
        package_api
    )
    all_repo_meta[package_name]["last_commit"] = issueProcess.get_last_commit(
        package_api
    )
    # Add github meta to review metadata
    review[package_name]["gh_meta"] = all_repo_meta[package_name]

# Export to yaml!
issueProcess.export_yaml("packages.yml", review)


# Breakpoints n next , s go inside function, C continue , L R run
# p variable name --> prints the value of the current variable
# Can also create conditional breakpoints...
