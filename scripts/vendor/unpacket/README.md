# Packet Tracer payload codec

The Python modules here are copied without modification from [Punkcake21/Unpacket](https://github.com/Punkcake21/Unpacket), revision `54cb6d6a9b46c6b4973356258cb8df6ae58b2ec7`. The [MIT license](LICENSE) applies to these files. No Cisco executable, firmware, installer or account data is included.

This codec reads saved lab data for evidence collection. A decoded XML structure or a successful encode/decode roundtrip does not establish that Packet Tracer opens the file or that its network works. Native application tests and their saved data stores are separate evidence.

Only the decoder modules required by the evidence collector are retained. The unused experimental encoder and native scaffold were removed during project cleanup.
