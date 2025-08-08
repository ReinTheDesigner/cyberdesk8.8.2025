on run {daemon_file, agent_file, user, cur_pid, source_dir}

  set unload_service to "launchctl unload -w /Library/LaunchDaemons/com.carriez.CyberDesk_service.plist || true;"

  set kill_others to "pgrep -x 'CyberDesk' | grep -v " & cur_pid & " | xargs kill -9;"

  set copy_files to "rm -rf /Applications/CyberDesk.app && ditto " & source_dir & " /Applications/CyberDesk.app && chown -R " & quoted form of user & ":staff /Applications/CyberDesk.app && xattr -r -d com.apple.quarantine /Applications/CyberDesk.app;"

  set sh1 to "echo " & quoted form of daemon_file & " > /Library/LaunchDaemons/com.carriez.CyberDesk_service.plist && chown root:wheel /Library/LaunchDaemons/com.carriez.CyberDesk_service.plist;"

  set sh2 to "echo " & quoted form of agent_file & " > /Library/LaunchAgents/com.carriez.CyberDesk_server.plist && chown root:wheel /Library/LaunchAgents/com.carriez.CyberDesk_server.plist;"

  set sh3 to "launchctl load -w /Library/LaunchDaemons/com.carriez.CyberDesk_service.plist;"

  set sh to unload_service & kill_others & copy_files & sh1 & sh2 & sh3

  do shell script sh with prompt "CyberDesk wants to update itself" with administrator privileges
end run
