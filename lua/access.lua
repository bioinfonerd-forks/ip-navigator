-- -*- coding: utf-8 -*-
-- (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
--[[

(c) 2013, Stavros Korokithakis
http://www.stavros.io/posts/writing-an-nginx-authentication-module-in-lua/

(c) 2013, phear
https://github.com/phaer/nginx-lua-auth

]]

-- Some variable declarations.
local cookie = ngx.var.cookie_Auth
local hmac = ""
local timestamp = ""

-- always permit access to the authentication endpoint
if ngx.var.uri == "/auth" then
    return
end

-- Check that the cookie exists.
if cookie ~= nil and cookie:find(":") ~= nil then
    -- If there's a cookie, split off the HMAC signature
    -- and timestamp.
    local divider = cookie:find(":")
    hmac = ngx.decode_base64(cookie:sub(divider+1))
    timestamp = cookie:sub(0, divider-1)

    -- Verify that the signature is valid.
    if ngx.hmac_sha1(ngx.var.lua_auth_secret, timestamp) == hmac and tonumber(timestamp) >= ngx.time() then
        return
    end
end

-- Internally rewrite the URL so that we serve
-- /auth/ if there's no valid token.
ngx.log(ngx.INFO, 'Require authentication to "' .. ngx.var.request_uri .. '"')
ngx.exec("/auth")
