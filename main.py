from github import Github
import requests
import re
import sys


def add_user_to_organization(members, permission, comment):
    try:
        for member in members:
            if member:
                try:
                    user_to_org = git_hub.get_organization(org_name)
                    user = git_hub.get_user(member)
                    # print(user_to_org.add_to_members(user, role=permission))
                    print(user_to_org.add_to_members(user))
                    if user_to_org is not None:
                        comment.append("Invitation has been sent to the user --> {}".format(member))
                        print("Invitation has been sent to the user.")
                    else:
                        comment.append("Some error Occured --> {},{}".format(user_to_org, member))
                        print(user_to_org)
                except Exception as error:
                    comment.append("Some error Occured --> {},{}".format(user_to_org, member))
                    print(error)
        return comment
    except Exception as error:
        comment.append("Exception --> {}".format(error))
        print(error)
        return comment
        
def add_user_to_team(members, teams_dic, comment):
    try:
        for team in teams_dic:
            if team:
                for member in members:
                    if member:
                        try:
                            org_team_ = git_hub.get_organization(org_name).get_team_by_slug(team)
                            user = git_hub.get_user(member)
                            print("adding user in a team ......", member)
                            user_to_team = org_team_.add_membership(user)
                            if user_to_team is None:
                                if org_team_.invitations().totalCount == 0:
                                    comment.append("User {} has been Added to the team --> {}".format(user, team))
                                    # jira.add_comment(issueKey, body="User {} has been Added to the team --> {}".format(user, team))
                                    print("User Has Been Added")
                                else:
                                    for i in org_team_.invitations():
                                        if i.login == member:
                                            comment.append("Invitation has been sent to the user --> {}".format(member))
                                            # jira.add_comment(issueKey, body="Invitation has been sent to the user --> {}".format(member))
                                            print("User Has Been Invited")
                            else:
                                comment.append("Some error Occured --> {}, {}, {}".format(user_to_org, team, member))
                                # jira.add_comment(issueKey, body="Some error Occured --> {}, {}, {}".format(user_to_org, team, member))
                                error_count += 1
                                print(user_to_team)
                        except Exception as error:
                            comment.append("Exception --> {}, {}, {}".format(error, team, member))
                            # jira.add_comment(issueKey, body="Exception --> {}, {}, {}".format(error, team, member))
                            error_count += 1
                            print(error)
        return error_count, comment  
    except Exception as error:
        jira.add_comment(issueKey, body="Exception --> {}".format(error))
        error_count += 1
        print(error)

        
def add_user_to_repo(members, repos, permission, error_count, comment):
    try:
        for member in members:
            if member:
                for repo in repos:
                    if repo:
                        try:
                            org = git_hub.get_organization(org_name).get_repo(repo)
                            user_to_repo = org.add_to_collaborators(member, permission=permission)
                            if user_to_repo is None:
                                print(member, " Has Been Added In ", repo)
                                comment.append("{0} Has Been Added In {1}".format(member, repo))
                                # jira.add_comment(issueKey, body="{0} Has Been Added In {1}".format(member, repo))
                            elif user_to_repo.id:
                                comment.append("{0} Has Been Invited {1} with Invite ID : {2}".format(member, repo, user_to_repo.id))
                                # jira.add_comment(issueKey, body="{0} Has Been Invited {1} with Invite ID : {2}".format(member, repo, user_to_repo.id))
                                print(member, " Has Been Invited In ", repo, " With Invite ID : ", user_to_repo.id)
                            else:
                                comment.append("Some error Occured --> {}, {}, {} ".format(user_to_repo, member, repo))
                                # jira.add_comment(issueKey, body="Some error Occured --> {}, {}, {} ".format(user_to_repo, member, repo))
                                error_count += 1
                                print(user_to_repo)
                        except Exception as error:
                            comment.append("Exception --> {}, {}, {}".format(error, member, repo))
                            # jira.add_comment(issueKey, body="Exception --> {}, {}, {}".format(error, member, repo))
                            error_count += 1
                            print(error)
        return error_count, comment
    except Exception as error:
        jira.add_comment(issueKey, body="Exception --> {}".format(error))
        error_count += 1
        print(error)


def add_team_to_repo(teams_dic, repos, permission, error_count, comment):
    try:
        for team in teams_dic:
            if team:
                org_team = git_hub.get_organization(org_name).get_team_by_slug(team)
                for repo in repos:
                    if repo:
                        try:
                            repo_ = git_hub.get_organization(org_name).get_repo(repo)
                            repo_count = org_team.repos_count
                            if org_team.update_team_repository(repo_, permission) == True:
                                if org_team.repos_count == repo_count + 1:
                                    comment.append("Repository --> {0}  Has Been Added into Team --> {1}!!".format(repo, team))
                                    # jira.add_comment(issueKey, body="Repository --> {0}  Has Been Added into Team --> {1}!!".format(repo, team))
                                    print("Repository --> {0}  Has Been Added into Team --> {1}!!".format(repo, team))
                        except Exception as error:
                            comment.append("Exception --> {}, {}, {}".format(error, team, repo))
                            # jira.add_comment(issueKey, body="Exception --> {}, {}, {}".format(error, team, repo))
                            error_count += 1
                            print(error)
        return error_count, comment
    except Exception as error:
        jira.add_comment(issueKey, body="Exception --> {}".format(error))
        error_count += 1
        print(error)


def user_to_branch_protection_rule(members, repos, branches, error_count, comment):
    try:
        for member in members:
            if member:
                for repo in repos:
                    if repo:
                        for branch in branches:
                            if branch:
                                try:
                                    org = git_hub.get_organization(org_name).get_repo(repo)
                                    branch_protection = org.get_branch(branch)
                                    response = branch_protection.add_user_push_restrictions(member)
                                    comment.append(response)
                                    print(response)
                                except Exception as error:
                                    comment.append("Exception --> {}, {}, {}, {}".format(error, member, repo, branch))
                                    # jira.add_comment(issueKey, body="Exception --> {}, {}, {}, {}".format(error, member, repo, branch))
                                    error_count += 1
                                    print(error)
        return error_count, comment
    except Exception as error:
        jira.add_comment(issueKey, body="Exception --> {}".format(error))
        error_count += 1
        print(error)


def create_repo(repository, description, error_count, comment):
    try:
        organization = git_hub.get_organization(org_name)
        for name in repository:
            print(name)
            organization.create_repo(name, description=description, private=True)
            print(organization)
            if organization:
                comment.append("Response -->  Repository Has Been Create !! {}".format(organization))
                # jira.add_comment(issueKey, body="Response -->  Repository Has Been Create !! {}".format(organization))
        return error_count, comment

    except Exception as error:
        comment.append("Exception --> {}".format(error))
        # jira.add_comment(issueKey, body="Exception --> {}".format(error))
        error_count += 1
        print(error)
        return error_count, comment
   


# def protect_matching_branches():
#     branch = 'staging_release'
#     c = 0
#     b_with_s_r = []
#     b_without_s_r = []
#     org = git_hub.get_organization(org_name).get_repos()
#     for i in org:
#         c = c + 1
#         try:
#             org = git_hub.get_organization(org_name).get_repo(i.name)
#             branch_protection = org.get_branch(branch)
#             branch_protection.edit_required_pull_request_reviews(dismiss_stale_reviews=True)
#             print(c, i.name)
#             b_with_s_r.append(i.name)
#         except Exception as e:
#             b_without_s_r.append(i.name)
#             print(e, c, i.name)

#     print("WITH STAGING RELEASE", b_with_s_r)
#     print("WITHOUT STAGING RELEASE", b_without_s_r)


if __name__ == "__main__":
    USERNAME = '#GTIHUB_USERNAME'
    access_token = sys.argv[1]
    git_hub = Github(USERNAME, access_token)
    
    if sys.argv[1] == '--Add-user-to-org':
        username = sys.argv[2]
        members = [str(i) for i in username.strip().split(",")]
        permission = sys.argv[3]

        add_user_to_organization(members, permission)

    if sys.argv[1] == '--Add-user-to-team':
        username = sys.argv[2]
        teamname = sys.argv[3]

        members = [str(i) for i in username.strip().split(",")]
        teams_dic = [str(i) for i in teamname.strip().split(",")]

        print("members = ", members)
        print("teams_dic = ", teams_dic)

        add_user_to_team(members, teams_dic)

    if sys.argv[1] == '--Add-team-to-repo':
        teamname = sys.argv[2]
        reponame = sys.argv[3]
        permission = sys.argv[4]

        teams_dic = [str(i) for i in teamname.strip().split(",")]
        repos = [str(i) for i in reponame.strip().split(",")]

        print("teams_dic = ", teams_dic)
        print("repos = ", repos)

        add_team_to_repo(teams_dic, repos, permission)

    if sys.argv[1] == '--Add-user-to-repo':
        username = sys.argv[2]
        reponame = sys.argv[3]
        permission = sys.argv[4]

        members = [str(i) for i in username.strip().split(",")]
        repos = [str(i) for i in reponame.strip().split(",")]

        print("members = ", members)
        print("repos = ", repos)

        def add_user_to_repo(members, repos, permission)

    if sys.argv[1] == '--User-to-Branch':
        username = sys.argv[2]
        reponame = sys.argv[3]
        branchname = sys.argv[4]

        members = [str(i) for i in username.strip().split(",")]
        repos = [str(i) for i in reponame.strip().split(",")]
        branches = [str(i) for i in branchname.strip().split(",")]

        print("members = ", members)
        print("repos = ", repos)
        print("branches = ", branches)
        
        user_to_branch_protection_rule(members, repos, branches)
        
        
    if sys.argv[1] == '--create-repo':
        repository = sys.argv[2]
        description = sys.argv[3]
        
        create_repo(repository, description)
        
        
        
