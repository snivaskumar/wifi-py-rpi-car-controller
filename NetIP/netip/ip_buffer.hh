/* Copyright (c) 2018 Francis James Franklin
 * 
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification, are permitted provided
 * that the following conditions are met:
 * 
 * 1. Redistributions of source code must retain the above copyright notice, this list of conditions and
 *    the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
 *    the following disclaimer in the documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
 * NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef __ip_buffer_hh__
#define __ip_buffer_hh__

#include "ip_header.hh"

class IP_Buffer : public Link {
private:
  u8_t buffer[IP_Buffer_WordCount << 1];

  u16_t buffer_length;

public:
  inline const u8_t * bytes () const {
    return (u8_t *) buffer;
  }
  inline u16_t length () const {
    return buffer_length;
  }

  inline void clear () {
    buffer_length = 0;
  }

  inline void append (u8_t * ptr, u16_t length) {
    if (ptr && length) {
      if (buffer_length + length <= (IP_Buffer_WordCount << 1)) {
	memcpy (buffer + buffer_length, ptr, length);
	buffer_length += length;
      }      
    }
  }

  IP_Buffer () :
    buffer_length(0)
  {
    // ...
  }

  ~IP_Buffer () {
    // ...
  }
};

class IP_BufferIterator : public BufferIterator {
public:
  IP_BufferIterator (const IP_Buffer & B) :
    BufferIterator(B.bytes (), B.length ())
  {
    // ...
  }

  ~IP_BufferIterator () {
    // ...
  }

  inline void ns16 (ns16_t & value) {
    value = *this;
    ++(*this);
    ++(*this);
  }

  inline void ns32 (ns32_t & value) {
    value = *this;
    *this += 4;
  }

  inline void address (IP_Address & value) {
    value = *this;
    *this += value.byte_length ();
  }
};

#endif /* ! __ip_buffer_hh__ */