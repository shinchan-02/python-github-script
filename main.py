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
                                    
                                    print("User Has Been Added")
                                else:
                                    for i in org_team_.invitations():
                                        if i.login == member:
                                            comment.append("Invitation has been sent to the user --> {}".format(member))
                                            
                                            print("User Has Been Invited")
                            else:
                                comment.append("Some error Occured --> {}, {}, {}".format(user_to_org, team, member))
                                
                                
                                print(user_to_team)
                        except Exception as error:
                            comment.append("Exception --> {}, {}, {}".format(error, team, member))                           
                            print(error)
        return comment  
    except Exception as error:        
        comment.append("Exception --> {}".format(error))
        print(error)
        retun comment

        
def add_user_to_repo(members, repos, permission, comment):
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
                                
                            elif user_to_repo.id:
                                comment.append("{0} Has Been Invited {1} with Invite ID : {2}".format(member, repo, user_to_repo.id))                               
                                print(member, " Has Been Invited In ", repo, " With Invite ID : ", user_to_repo.id)
                            else:
                                comment.append("Some error Occured --> {}, {}, {} ".format(user_to_repo, member, repo))                               
                                print(user_to_repo)
                        except Exception as error:
                            comment.append("Exception --> {}, {}, {}".format(error, member, repo))
                            
                            
                            print(error)
        return comment
    except Exception as error:               
        comment.append("Exception --> {}".format(error))
        print(error)
        retun comment


def add_team_to_repo(teams_dic, repos, permission, comment):
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
                                    print("Repository --> {0}  Has Been Added into Team --> {1}!!".format(repo, team))
                        except Exception as error:
                            comment.append("Exception --> {}, {}, {}".format(error, team, repo))
                            print(error)
        return comment
    except Exception as error:
        comment.append("Exception --> {}".format(error))
        print(error)
        retun comment


def user_to_branch_protection_rule(members, repos, branches, comment):
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
                                    print(error)
        return comment
    except Exception as error:
        comment.append("Exception --> {}".format(error))
        print(error)
        retun comment


def create_repo(repository, description, comment):
    try:
        organization = git_hub.get_organization(org_name)
        for name in repository:
            print(name)
            organization.create_repo(name, description=description, private=True)
            print(organization)
            if organization:
                comment.append("Response -->  Repository Has Been Create !! {}".format(organization))
        return comment

    except Exception as error:
        comment.append("Exception --> {}".format(error))
        print(error)
        retun comment
   

if __name__ == "__main__":
    USERNAME = '#GTIHUB_USERNAME'
    access_token = sys.argv[1]
    git_hub = Github(USERNAME, access_token)
    
    if sys.argv[1] == '--Add-user-to-org':
        username = sys.argv[2]
        members = [str(i) for i in username.strip().split(",")]
        permission = sys.argv[3]

        comment = add_user_to_organization(members, permission)

    if sys.argv[1] == '--Add-user-to-team':
        username = sys.argv[2]
        teamname = sys.argv[3]

        members = [str(i) for i in username.strip().split(",")]
        teams_dic = [str(i) for i in teamname.strip().split(",")]

        print("members = ", members)
        print("teams_dic = ", teams_dic)

        comment = add_user_to_team(members, teams_dic)

    if sys.argv[1] == '--Add-team-to-repo':
        teamname = sys.argv[2]
        reponame = sys.argv[3]
        permission = sys.argv[4]

        teams_dic = [str(i) for i in teamname.strip().split(",")]
        repos = [str(i) for i in reponame.strip().split(",")]

        print("teams_dic = ", teams_dic)
        print("repos = ", repos)

        comment = add_team_to_repo(teams_dic, repos, permission)

    if sys.argv[1] == '--Add-user-to-repo':
        username = sys.argv[2]
        reponame = sys.argv[3]
        permission = sys.argv[4]

        members = [str(i) for i in username.strip().split(",")]
        repos = [str(i) for i in reponame.strip().split(",")]

        print("members = ", members)
        print("repos = ", repos)

        comment = add_user_to_repo(members, repos, permission)

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
        
        comment = user_to_branch_protection_rule(members, repos, branches)
        
        
    if sys.argv[1] == '--create-repo':
        repository = sys.argv[2]
        description = sys.argv[3]
        
        comment = create_repo(repository, description)
        
