#!/usr/bin/env ruby
#
require 'sinatra'
require 'net/imap'
require 'mail'
require 'mail/encodings'
require 'time'
require 'json'

get "/mail/#{ENV["SECRET_KEY"]}" do
  content_type 'application/json'

  list_mail.to_json
end

def list_mail
  imap = Net::IMAP.new(ENV["IMAP_HOST"], 993, true)
  imap.login(ENV["IMAP_USERNAME"], ENV["IMAP_PASSWORD"])
  imap.examine("Inbox")
  uids = imap.search("ALL")
  mails = imap.fetch(uids, ["ENVELOPE", "FLAGS"])
  imap.logout
  imap.disconnect

  mails.map do |fetchdata|
    {
      "from" => fetchdata.attr["ENVELOPE"].from.map do |addr|
        name = addr.name
        name = Mail::Encodings.value_decode(name) if name
        [name, "<#{addr.mailbox}@#{addr.host}>"].compact.join(" ")
      end.first,
      "subject" => Mail::Encodings.value_decode(fetchdata.attr["ENVELOPE"].subject),
      "date" => Time.rfc2822(fetchdata.attr["ENVELOPE"].date).localtime.to_s,
      "flags" => fetchdata.attr["FLAGS"].grep(Symbol),
    }
  end.sort_by { |mail| mail["date"] }.reverse
end
